"""Hybrid STT engine ??Vosk X-Vector speaker diarization + Whisper.cpp STT.

This is the crown jewel of termux-stt: a single ``create_engine("hybrid")``
call gives you high-accuracy transcription **and** speaker diarization
using less than 1.5 GB of RAM on a mobile device.

Pipeline
--------
1. Preprocess audio ??16 kHz mono WAV
2. Silero-VAD silence filtering
3. Vosk SpkModel ??128-d X-Vector per chunk
4. Pure-Python K-Means clustering (no numpy/sklearn)
5. Whisper.cpp STT with timestamps
6. SpeakerMapper aligns clusters to transcript segments
7. Returns ``DiarizedResult``
"""

import logging
from typing import Any, Dict, Iterator, Optional

from termux_stt.engine.base import Engine, EngineConfig
from termux_stt.export.result import DiarizedResult, Segment, TranscriptResult

logger = logging.getLogger(__name__)

__all__ = ['HybridEngine']


class HybridEngine(Engine):
    """Vosk (X-Vector) + Whisper (STT) hybrid diarization engine.

    Combines the ultra-lightweight Vosk speaker embeddings (220 MB RAM)
    with high-accuracy Whisper transcription to produce speaker-labelled
    transcripts on mobile hardware.
    """

    def __init__(self, config: EngineConfig) -> None:
        self.config = config

        # Build separate configs for each sub-engine
        whisper_config = EngineConfig(
            engine='whisper',
            model=config.model,
            lang=config.lang,
            threads=config.threads,
            vad=config.vad,
            vad_threshold=config.vad_threshold,
            quantization=config.quantization,
        )
        vosk_config = EngineConfig(
            engine='vosk',
            model='small-ko-0.22',
            lang=config.lang,
            num_speakers=config.num_speakers or 2,
        )

        from termux_stt.engine.vosk_engine import VoskEngine
        from termux_stt.engine.whisper_engine import WhisperEngine

        self._whisper = WhisperEngine(whisper_config)
        self._vosk = VoskEngine(vosk_config)

    # ------------------------------------------------------------------
    # Core engine methods
    # ------------------------------------------------------------------

    def transcribe(self, audio_path: str, **kwargs: Any) -> TranscriptResult:
        """Transcribe audio using Whisper STT only (no diarization)."""
        return self._whisper.transcribe(audio_path, **kwargs)

    def diarize(
        self, audio_path: str, num_speakers: int = 2, allow_fallback: bool = False, **kwargs: Any
    ) -> DiarizedResult:
        """Full hybrid pipeline: STT + speaker diarization.

        Parameters
        ----------
        audio_path : str
            Path to an audio file.
        num_speakers : int
            Expected number of distinct speakers.
        allow_fallback : bool
            Whether to allow pause-heuristic fallback when X-Vector extraction fails.

        Returns
        -------
        DiarizedResult
            Transcript segments with ``speaker`` labels assigned.
        """
        from termux_stt.audio.preprocessor import preprocess
        from termux_stt.diarization.clustering import KMeans
        from termux_stt.diarization.mapper import SpeakerMapper

        # 1. Preprocess
        wav_path = preprocess(audio_path, target_sr=16000, force_mono=True)
        import os
        is_temp_wav = os.path.abspath(wav_path) != os.path.abspath(audio_path)

        try:
            # 2. Vosk X-Vector extraction
            xvectors = []
            try:
                xvectors = self._vosk.extract_xvectors(wav_path, chunk_sec=2.0)
            except Exception as exc:
                if not allow_fallback:
                    raise RuntimeError(
                        f"X-Vector speaker embedding extraction failed: {exc}. "
                        f"Ensure vosk-model-spk is installed or pass allow_fallback=True."
                    )
                logger.warning("X-Vector extraction failed: %s ??speaker diarization falling back to Speaker_Unknown", exc)

            # 3. Pure Python K-Means clustering
            speaker_labels = []
            if xvectors and len(xvectors) >= num_speakers:
                vectors = [xv[2] for xv in xvectors]  # (start, end, vector)
                kmeans = KMeans(n_clusters=num_speakers)
                kmeans.fit(vectors)

                speaker_labels = [
                    (xv[0], xv[1], label)
                    for xv, label in zip(xvectors, kmeans.labels_)
                ]
            elif xvectors:
                # Fewer chunks than speakers ??assign adaptive clusters
                kmeans = KMeans(n_clusters=num_speakers)
                kmeans.fit([xv[2] for xv in xvectors])
                speaker_labels = [
                    (xv[0], xv[1], label)
                    for xv, label in zip(xvectors, kmeans.labels_)
                ]

            # 4. Whisper STT transcription
            stt_result = self._whisper.transcribe(wav_path, **kwargs)

            # 5. Align speakers to transcript segments
            mapper = SpeakerMapper()
            aligned = mapper.align(stt_result.segments, speaker_labels, num_speakers=num_speakers)

            # 6. Build result
            unique_speakers = sorted(
                set(s.speaker for s in aligned if s.speaker)
            )

            return DiarizedResult(
                text=" ".join(s.text for s in aligned),
                language=stt_result.language,
                segments=aligned,
                duration=stt_result.duration,
                speakers=unique_speakers,
            )
        finally:
            if is_temp_wav and os.path.exists(wav_path):
                try:
                    os.remove(wav_path)
                except OSError as _tmp_del_err:
                    import logging; logging.getLogger(__name__).debug("temp file cleanup OSError: %s", _tmp_del_err)

    def stream_mic(
        self, duration: Optional[float] = None
    ) -> Iterator[Segment]:
        """Stream transcription from the microphone (Whisper only)."""
        return self._whisper.stream_mic(duration=duration)

    def stream_file(
        self, audio_path: str, chunk_sec: float = 5.0
    ) -> Iterator[Segment]:
        """Stream transcription from a file (Whisper only)."""
        return self._whisper.stream_file(audio_path, chunk_sec=chunk_sec)

    def get_info(self) -> Dict[str, Any]:
        """Return engine status information."""
        return {
            "name": "Hybrid (Vosk X-Vector + Whisper STT)",
            "whisper": self._whisper.get_info(),
            "vosk": self._vosk.get_info(),
            "num_speakers": self.config.num_speakers,
        }
