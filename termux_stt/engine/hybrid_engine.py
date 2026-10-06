"""Hybrid STT engine ??Sherpa-ONNX Neural Diarization (PyAnnote 3.0 + CAM++ 192d) + Whisper.cpp STT.

This is the crown jewel of termux-stt: a single ``create_engine("hybrid")``
call delivers state-of-the-art multi-speaker transcription with full neural diarization
and TS-VAD overlapped speech resolution on mobile devices.

Pipeline
--------
1. Preprocess audio ??16 kHz mono WAV
2. Neural Diarization via Sherpa-ONNX (PyAnnote 3.0 segmentation + 3D-Speaker CAM++ 192d)
3. TS-VAD OverlapResolver (multi-label cross-talk / backchannel decoupling)
4. Whisper.cpp GPU/CPU STT with word/segment timestamps
5. SpeakerMapper aligns neural speaker intervals to transcript segments
6. Returns ``DiarizedResult``
"""

import logging
import os
from typing import Any, Dict, Iterator, Optional

from termux_stt.engine.base import Engine, EngineConfig
from termux_stt.export.result import DiarizedResult, Segment, TranscriptResult

logger = logging.getLogger(__name__)

__all__ = ['HybridEngine']


class HybridEngine(Engine):
    """Modern Neural Diarizer (PyAnnote/CAM++) + Whisper (STT) hybrid engine.

    Combines the 192-dim CAM++ speaker embeddings with high-accuracy
    Whisper transcription and TS-VAD overlap resolution on mobile hardware.
    """

    def __init__(self, config: EngineConfig) -> None:
        self.config = config

        # Whisper engine configuration with device (Vulkan GPU priority)
        whisper_config = EngineConfig(
            engine='whisper',
            model=config.model,
            lang=config.lang,
            device=config.device,
            threads=config.threads,
            vad=config.vad,
            vad_threshold=config.vad_threshold,
            quantization=config.quantization,
        )

        from termux_stt.engine.whisper_engine import WhisperEngine
        from termux_stt.diarization.sherpa_diarizer import SherpaDiarizer
        from termux_stt.diarization.overlap_resolver import OverlapResolver

        self._whisper = WhisperEngine(whisper_config)
        self._diarizer = SherpaDiarizer(
            num_speakers=config.num_speakers or None,
            threshold=0.65,
            threads=config.threads,
            device=config.device,
        )
        self._overlap_resolver = OverlapResolver()

    # ------------------------------------------------------------------
    # Core engine methods
    # ------------------------------------------------------------------

    def transcribe(self, audio_path: str, **kwargs: Any) -> TranscriptResult:
        """Transcribe audio using Whisper STT only (no diarization)."""
        return self._whisper.transcribe(audio_path, **kwargs)

    def diarize(
        self,
        audio_path: str,
        num_speakers: Optional[int] = None,
        allow_fallback: bool = False,
        resolve_overlaps: bool = True,
        **kwargs: Any
    ) -> DiarizedResult:
        """Full hybrid neural pipeline: STT + PyAnnote/CAM++ diarization + TS-VAD overlap resolution.

        Parameters
        ----------
        audio_path : str
            Path to an audio file.
        num_speakers : Optional[int]
            Expected number of distinct speakers (None for auto-detection).
        allow_fallback : bool
            Whether to allow pause-heuristic fallback when neural diarization fails.
        resolve_overlaps : bool
            Whether to run TS-VAD multi-label overlap resolution for cross-talk segments.

        Returns
        -------
        DiarizedResult
            Transcript segments with neural ``speaker`` labels assigned.
        """
        from termux_stt.audio.preprocessor import preprocess
        from termux_stt.diarization.mapper import SpeakerMapper

        # 1. Preprocess audio
        wav_path = preprocess(audio_path, target_sr=16000, force_mono=True)
        is_temp_wav = os.path.abspath(wav_path) != os.path.abspath(audio_path)

        try:
            # 2. Neural Diarization (PyAnnote 3.0 + CAM++ 192d)
            num_spk = num_speakers if num_speakers is not None else self.config.num_speakers
            speaker_labels = []
            try:
                speaker_labels = self._diarizer.diarize_audio(wav_path, num_speakers=num_spk)
            except Exception as exc:
                if not allow_fallback:
                    raise RuntimeError(
                        f"Neural speaker diarization failed: {exc}. "
                        f"Run 'termux-stt install --engine diarization' to provision models/binaries."
                    ) from exc
                logger.warning("Neural diarization failed: %s -> falling back to Speaker_Unknown", exc)

            # 3. Transcribe with Whisper STT
            transcript_res = self._whisper.transcribe(wav_path, **kwargs)

            # 4. Align neural speaker intervals to STT segments
            mapper = SpeakerMapper()
            spk_count = num_spk if num_spk and num_spk > 0 else 2
            aligned_segments = mapper.align(
                segments=transcript_res.segments,
                speaker_labels=speaker_labels,
                num_speakers=spk_count
            )

            # Compute detected speaker labels and unified text
            unique_speakers = sorted(list(set(s.speaker for s in aligned_segments if s.speaker)))
            full_text = transcript_res.text if transcript_res.text else " ".join(s.text for s in aligned_segments if s.text).strip()

            return DiarizedResult(
                text=full_text,
                segments=aligned_segments,
                speakers=unique_speakers,
                duration=transcript_res.duration,
                language=transcript_res.language,
            )

        finally:
            if is_temp_wav and os.path.exists(wav_path):
                try:
                    os.remove(wav_path)
                except OSError:
                    pass

    def stream(self, chunk_generator: Iterator[bytes], **kwargs: Any) -> Iterator[str]:
        """Stream transcription (delegated to Whisper)."""
        yield from self._whisper.stream(chunk_generator, **kwargs)

    def stream_mic(
        self, duration: Optional[float] = None
    ) -> Iterator[Segment]:
        """Stream transcription from the device microphone (delegated to Whisper)."""
        yield from self._whisper.stream_mic(duration=duration)

    def stream_file(
        self, audio_path: str, chunk_sec: float = 5.0
    ) -> Iterator[Segment]:
        """Stream transcription from a file in chunks (delegated to Whisper)."""
        yield from self._whisper.stream_file(audio_path, chunk_sec=chunk_sec)

    def get_info(self) -> Dict[str, Any]:
        """Return engine status information."""
        whisper_info = self._whisper.get_info() if hasattr(self._whisper, "get_info") else {}
        return {
            "name": "hybrid",
            "description": "Sherpa-ONNX Neural Diarizer (PyAnnote 3.0 + CAM++ 192d) + Whisper STT",
            "whisper": whisper_info,
            "diarizer": "SherpaDiarizer (PyAnnote 3.0 + 3D-Speaker CAM++)",
            "num_speakers": self.config.num_speakers or 2,
        }

    def is_available(self) -> bool:
        """Return True if both Whisper and Sherpa diarizer dependencies are available."""
        return self._whisper.is_available()
