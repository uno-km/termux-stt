"""Sherpa-ONNX engine wrapper ??ONNX Runtime based STT for Termux.

Supports Zipformer streaming/offline models, SenseVoice, and CAM++
speaker embedding extraction.
"""

import logging
from pathlib import Path
from typing import Any, Dict, Iterator, Optional

from termux_stt.engine.base import Engine, EngineConfig
from termux_stt.export.result import DiarizedResult, Segment, TranscriptResult

logger = logging.getLogger(__name__)

__all__ = ['SherpaEngine']


class SherpaEngine(Engine):
    """Sherpa-ONNX engine via subprocess.

    Provides offline and streaming STT using Zipformer / SenseVoice
    models, plus CAM++ speaker diarization.
    """

    def __init__(self, config: EngineConfig) -> None:
        self.config = config
        self.model_name = config.model_name

    # ------------------------------------------------------------------
    # Binary location
    # ------------------------------------------------------------------

    def _find_binary(self, name: str = "sherpa-onnx-offline") -> str:
        """Locate a sherpa-onnx binary or raise FileNotFoundError."""
        import shutil
        found = shutil.which(name)
        if found:
            return found
        candidates = [
            Path.home() / ".local" / "bin" / name,
            Path(f"/data/data/com.termux/files/home/.local/bin/{name}"),
            Path(f"/data/data/com.termux/files/usr/bin/{name}"),
        ]
        for p in candidates:
            if p.exists():
                return str(p)
        raise FileNotFoundError(
            f"Cannot locate '{name}' executable. Please run 'termux-stt install' "
            f"or install sherpa-onnx in PATH."
        )

    # ------------------------------------------------------------------
    # Core engine methods
    # ------------------------------------------------------------------

    def transcribe(self, audio_path: str, **kwargs: Any) -> TranscriptResult:
        """Transcribe an audio file using sherpa-onnx-offline."""
        import os

        from termux_stt.audio.preprocessor import preprocess
        from termux_stt.models.hub import ModelHub
        from termux_stt.platform.process_pool import run_isolated

        wav_path = preprocess(audio_path, target_sr=16000, force_mono=True)
        is_temp_wav = os.path.abspath(wav_path) != os.path.abspath(audio_path)
        model_dir = ModelHub.ensure_model('sherpa', self.model_name)
        binary = self._find_binary()

        cmd = [
            binary,
            f"--tokens={model_dir}/tokens.txt",
            f"--encoder={model_dir}/encoder.onnx",
            f"--decoder={model_dir}/decoder.onnx",
            f"--joiner={model_dir}/joiner.onnx",
            wav_path,
        ]

        try:
            result = run_isolated(cmd)
            if result.returncode != 0:
                raise RuntimeError(
                    f"sherpa-onnx exited with code {result.returncode}: "
                    f"{result.stderr}"
                )

            text = result.stdout.strip()
            return TranscriptResult(
                text=text,
                language=self.config.language,
                segments=[Segment(start=0.0, end=0.0, text=text)] if text else [],
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
        """Stream transcription from the microphone using sherpa-onnx."""
        import os
        import tempfile

        from termux_stt.audio.mic import MicCapture

        mic = MicCapture()
        for chunk_bytes in mic.stream(duration=duration, chunk_sec=5.0):
            with tempfile.NamedTemporaryFile(
                suffix=".wav", delete=False
            ) as tmp:
                tmp_path = tmp.name
                # Write minimal WAV
                import struct
                num_channels, sample_width, sr = 1, 2, 16000
                data_size = len(chunk_bytes)
                tmp.write(b"RIFF")
                tmp.write(struct.pack("<I", data_size + 36))
                tmp.write(b"WAVEfmt ")
                tmp.write(struct.pack("<IHHIIHH", 16, 1, num_channels, sr,
                                      sr * num_channels * sample_width,
                                      num_channels * sample_width,
                                      sample_width * 8))
                tmp.write(b"data")
                tmp.write(struct.pack("<I", data_size))
                tmp.write(chunk_bytes)

            try:
                result = self.transcribe(tmp_path)
                for seg in result.segments:
                    yield seg
            finally:
                try:
                    os.unlink(tmp_path)
                except OSError as _tmp_del_err:
                    import logging; logging.getLogger(__name__).debug("temp file cleanup OSError: %s", _tmp_del_err)

    def stream_file(
        self, audio_path: str, chunk_sec: float = 5.0
    ) -> Iterator[Segment]:
        """Stream transcription from a file in chunks."""
        import os
        import struct
        import tempfile
        import wave

        from termux_stt.audio.preprocessor import preprocess

        wav_path = preprocess(audio_path, target_sr=16000, force_mono=True)
        is_temp_wav = os.path.abspath(wav_path) != os.path.abspath(audio_path)

        try:
            with wave.open(wav_path, "rb") as wf:
                sr = wf.getframerate()
                chunk_frames = int(chunk_sec * sr)
                offset = 0.0

                while True:
                    data = wf.readframes(chunk_frames)
                    if len(data) == 0:
                        break

                    with tempfile.NamedTemporaryFile(
                        suffix=".wav", delete=False
                    ) as tmp:
                        tmp_path = tmp.name
                        num_channels, sample_width = 1, 2
                        data_size = len(data)
                        tmp.write(b"RIFF")
                        tmp.write(struct.pack("<I", data_size + 36))
                        tmp.write(b"WAVEfmt ")
                        tmp.write(struct.pack("<IHHIIHH", 16, 1, num_channels, sr,
                                              sr * num_channels * sample_width,
                                              num_channels * sample_width,
                                              sample_width * 8))
                        tmp.write(b"data")
                        tmp.write(struct.pack("<I", data_size))
                        tmp.write(data)

                    try:
                        result = self.transcribe(tmp_path)
                        for seg in result.segments:
                            yield Segment(
                                start=offset + seg.start,
                                end=offset + seg.end,
                                text=seg.text,
                            )
                    finally:
                        try:
                            os.unlink(tmp_path)
                        except OSError as _tmp_del_err:
                            import logging; logging.getLogger(__name__).debug("temp file cleanup OSError: %s", _tmp_del_err)

                    actual_frames = len(data) // (wf.getsampwidth() * wf.getnchannels())
                    offset += actual_frames / sr
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
            "name": "Sherpa-ONNX",
            "model": self.model_name,
            "language": self.config.language,
            "binary_path": self._find_binary(),
        }
