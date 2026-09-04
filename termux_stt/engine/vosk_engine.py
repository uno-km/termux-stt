"""Vosk STT engine wrapper with X-Vector speaker embedding extraction.

Handles the ``sys.platform`` spoofing required for Vosk on Android Termux
and provides both speech-to-text and 128-dimensional X-Vector extraction.
"""

import json
import logging
import os
import sys
import wave
from typing import Any, Dict, Iterator, List, Optional, Tuple

from termux_stt.engine.base import Engine, EngineConfig
from termux_stt.export.result import DiarizedResult, Segment, TranscriptResult

logger = logging.getLogger(__name__)

__all__ = ['VoskEngine']


class VoskEngine(Engine):
    """Vosk engine for STT and X-Vector speaker embeddings.

    Automatically applies ``sys.platform = 'linux'`` spoofing required
    for the Vosk binary to load on Android/Termux.  Provides both
    standard transcription and 128-dimensional X-Vector extraction for
    use in the hybrid speaker diarization pipeline.
    """

    def __init__(self, config: EngineConfig) -> None:
        self._spoof_platform()
        self.config = config
        self.model_name = config.model_name
        self._model = None
        self._spk_model = None

    # ------------------------------------------------------------------
    # Lazy model loading
    # ------------------------------------------------------------------

    def _ensure_model(self) -> None:
        """Lazily load the Vosk model on first use."""
        if self._model is not None:
            return
        try:
            import vosk

            from termux_stt.models.hub import ModelHub

            model_path = ModelHub.ensure_model('vosk', self.model_name)
            self._model = vosk.Model(model_path)

            # Load speaker model when diarization is requested
            if self.config.num_speakers > 0:
                spk_path = ModelHub.ensure_model('vosk', 'vosk-model-spk-0.4')
                self._spk_model = vosk.SpkModel(spk_path)
        except ImportError:
            logger.warning(
                "Vosk module not installed. Run 'termux-stt-install' "
                "or install vosk manually."
            )
        except Exception as exc:
            logger.error(f"Failed to load Vosk model: {exc}")

    @staticmethod
    def _spoof_platform() -> None:
        """Spoof ``sys.platform`` to ``'linux'`` only on Android / Termux."""
        from termux_stt.platform.hardware import is_termux

        is_android = hasattr(os, "uname") and "android" in os.uname().release.lower()
        if (is_termux() or is_android) and 'linux' not in sys.platform:
            logger.info("Spoofing sys.platform to 'linux' for Vosk Android/Termux compatibility")
            sys.platform = 'linux'

    # ------------------------------------------------------------------
    # Core engine methods
    # ------------------------------------------------------------------

    def transcribe(self, audio_path: str, **kwargs: Any) -> TranscriptResult:
        """Transcribe an audio file using Vosk KaldiRecognizer."""
        from termux_stt.audio.preprocessor import preprocess

        self._ensure_model()
        if self._model is None:
            raise RuntimeError("Vosk model not initialized ??is vosk installed?")

        import vosk

        wav_path = preprocess(audio_path, target_sr=16000, force_mono=True)
        is_temp_wav = os.path.abspath(wav_path) != os.path.abspath(audio_path)

        try:
            with wave.open(wav_path, "rb") as wf:
                opts = {**self.config.extra, **kwargs}
                rec = vosk.KaldiRecognizer(self._model, wf.getframerate())
                rec.SetWords(opts.get("words", True))
                if "max_alternatives" in opts:
                    rec.SetMaxAlternatives(int(opts["max_alternatives"]))
                if "grammar" in opts:
                    import json as _json
                    grammar_val = opts["grammar"]
                    if isinstance(grammar_val, (list, dict)):
                        rec.SetGrammar(_json.dumps(grammar_val))
                    elif isinstance(grammar_val, str):
                        rec.SetGrammar(grammar_val)

                segments: List[Segment] = []
                texts: List[str] = []

                while True:
                    data = wf.readframes(4000)
                    if len(data) == 0:
                        break
                    if rec.AcceptWaveform(data):
                        res = json.loads(rec.Result())
                        text = res.get("text", "").strip()
                        words = res.get("result", [])
                        if words:
                            t0 = words[0].get("start", 0.0)
                            t1 = words[-1].get("end", 0.0)
                            segments.append(Segment(start=t0, end=t1, text=text))
                        elif text:
                            segments.append(Segment(start=0.0, end=0.0, text=text))
                        if text:
                            texts.append(text)

                # Capture final partial
                res = json.loads(rec.FinalResult())
                text = res.get("text", "").strip()
                words = res.get("result", [])
                if words:
                    t0 = words[0].get("start", 0.0)
                    t1 = words[-1].get("end", 0.0)
                    segments.append(Segment(start=t0, end=t1, text=text))
                elif text:
                    segments.append(Segment(start=0.0, end=0.0, text=text))
                if text:
                    texts.append(text)

            return TranscriptResult(
                text=" ".join(texts),
                language=self.config.language,
                segments=segments,
            )
        finally:
            if is_temp_wav and os.path.exists(wav_path):
                try:
                    os.remove(wav_path)
                except OSError as _tmp_del_err:
                    import logging; logging.getLogger(__name__).debug("temp file cleanup OSError: %s", _tmp_del_err)

    def extract_xvectors(
        self,
        audio_path: str,
        chunk_sec: float = 2.0,
    ) -> List[Tuple[float, float, List[float]]]:
        """Extract 128-dimensional X-Vector speaker embeddings.

        Parameters
        ----------
        audio_path : str
            Path to a 16 kHz mono WAV file.
        chunk_sec : float
            Duration of each analysis chunk in seconds.

        Returns
        -------
        list of (start, end, vector)
            Each entry is ``(start_sec, end_sec, 128d_float_list)``.
        """
        from termux_stt.audio.preprocessor import preprocess

        self._ensure_model()
        if self._model is None or self._spk_model is None:
            raise RuntimeError("Vosk model or SpkModel not initialised")

        import vosk

        wav_path = preprocess(audio_path, target_sr=16000, force_mono=True)
        is_temp_wav = os.path.abspath(wav_path) != os.path.abspath(audio_path)
        results: List[Tuple[float, float, List[float]]] = []
        offset = 0.0

        try:
            with wave.open(wav_path, "rb") as wf:
                sample_rate = wf.getframerate()
                chunk_frames = int(chunk_sec * sample_rate)

                while True:
                    data = wf.readframes(chunk_frames)
                    if len(data) == 0:
                        break

                    actual_frames = len(data) // (wf.getsampwidth() * wf.getnchannels())
                    end_time = offset + actual_frames / sample_rate

                    rec = vosk.KaldiRecognizer(self._model, sample_rate, self._spk_model)
                    rec.AcceptWaveform(data)
                    res = json.loads(rec.FinalResult())

                    spk_vector = res.get("spk", [0.0] * 128)
                    results.append((offset, end_time, spk_vector))

                    offset = end_time

            return results
        finally:
            if is_temp_wav and os.path.exists(wav_path):
                try:
                    os.remove(wav_path)
                except OSError as _tmp_del_err:
                    import logging; logging.getLogger(__name__).debug("temp file cleanup OSError: %s", _tmp_del_err)

    def stream_mic(
        self, duration: Optional[float] = None
    ) -> Iterator[Segment]:
        """Stream transcription from the device microphone via Vosk."""
        from termux_stt.audio.mic import MicCapture

        self._ensure_model()
        if self._model is None:
            raise RuntimeError("Vosk model not initialised")

        import vosk

        mic = MicCapture()
        rec = vosk.KaldiRecognizer(self._model, 16000)

        for chunk in mic.stream(duration=duration):
            if rec.AcceptWaveform(chunk):
                res = json.loads(rec.Result())
                text = res.get("text", "").strip()
                if text:
                    yield Segment(start=0.0, end=0.0, text=text)

    def stream_file(
        self, audio_path: str, chunk_sec: float = 5.0
    ) -> Iterator[Segment]:
        """Stream transcription from a file in chunks."""
        from termux_stt.audio.preprocessor import preprocess

        self._ensure_model()
        if self._model is None:
            raise RuntimeError("Vosk model not initialised")

        import vosk

        wav_path = preprocess(audio_path, target_sr=16000, force_mono=True)
        is_temp_wav = os.path.abspath(wav_path) != os.path.abspath(audio_path)

        try:
            with wave.open(wav_path, "rb") as wf:
                rec = vosk.KaldiRecognizer(self._model, wf.getframerate())
                chunk_frames = int(chunk_sec * wf.getframerate())

                while True:
                    data = wf.readframes(chunk_frames)
                    if len(data) == 0:
                        break
                    if rec.AcceptWaveform(data):
                        res = json.loads(rec.Result())
                        text = res.get("text", "").strip()
                        if text:
                            yield Segment(start=0.0, end=0.0, text=text)

                res = json.loads(rec.FinalResult())
                text = res.get("text", "").strip()
                if text:
                    yield Segment(start=0.0, end=0.0, text=text)
        finally:
            if is_temp_wav and os.path.exists(wav_path):
                try:
                    os.remove(wav_path)
                except OSError as _tmp_del_err:
                    import logging; logging.getLogger(__name__).debug("temp file cleanup OSError: %s", _tmp_del_err)

    def diarize(
        self, audio_path: str, num_speakers: int = 2, **kwargs: Any
    ) -> DiarizedResult:
        """Run STT with speaker diarization.

        Delegates to HybridEngine (Vosk X-Vector + Whisper STT) when available,
        or wraps transcript segments into a valid DiarizedResult.
        """
        try:
            from .hybrid_engine import HybridEngine
            hybrid = HybridEngine(self.config)
            return hybrid.diarize(audio_path, num_speakers=num_speakers, **kwargs)
        except Exception as exc:
            logger.debug("Hybrid diarization delegation unavailable (%s), falling back to standalone diarized result", exc)
            res = self.transcribe(audio_path, **kwargs)
            speaker_label = "Speaker_0" if num_speakers <= 1 else "Speaker_Unknown"
            diarized_segments = [
                Segment(
                    start=s.start,
                    end=s.end,
                    text=s.text,
                    speaker=speaker_label,
                    confidence=s.confidence,
                )
                for s in res.segments
            ]
            return DiarizedResult(
                text=res.text,
                language=res.language,
                segments=diarized_segments,
                duration=res.duration,
                speakers=[speaker_label] if diarized_segments else [],
            )

    def get_info(self) -> Dict[str, Any]:
        """Return engine status information."""
        return {
            "name": "Vosk",
            "model": self.model_name,
            "language": self.config.language,
            "spk_model_loaded": self._spk_model is not None,
            "platform_spoofed": True,
        }
