"""Whisper.cpp engine wrapper ??subprocess-isolated STT for Android Termux.

Runs ``whisper.cpp`` as an external process for crash isolation; a C++
segfault will never take down the Python host.
"""

import json
import logging
import os
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional

from termux_stt.engine.base import Engine, EngineConfig
from termux_stt.export.result import DiarizedResult, Segment, TranscriptResult
from termux_stt.platform.process_pool import run_isolated

logger = logging.getLogger(__name__)

__all__ = ['WhisperEngine']


class WhisperEngine(Engine):
    """whisper.cpp engine via subprocess with process isolation.

    Supports all GGML quantisation levels (f16, q8_0, q5_1, q4_0) and
    automatic ARM NEON / FP16 optimisation.
    """

    def __init__(self, config: EngineConfig) -> None:
        self.config = config
        self.model = config.model_name
        self.lang = config.language
        self.device = config.device

        # Hardware acceleration context delegation via ameva-runtime & SttAdapter
        dev_lower = str(self.device or "auto").strip().lower()
        self.ctx = None
        if dev_lower != "cpu":
            try:
                from ameva_runtime import vulkan as avr
                from ameva_runtime.vulkan.adapters import SttAdapter

                self.ctx = avr.get_or_create_context(self.device)
                report = getattr(self.ctx, "doctor", avr.Doctor()).run_self_test(verbose=False)
                binding_res = SttAdapter.bind(self, report)
                if dev_lower in ("gpu", "vulkan") and not getattr(binding_res, "is_vulkan", False):
                    raise RuntimeError(
                        f"[ZeroSilentFallback] Explicit GPU mode requested ('{self.device}'), "
                        f"but SttAdapter bound to non-Vulkan backend ('{getattr(binding_res, 'backend', 'unknown')}')."
                    )
            except Exception as exc:
                if dev_lower in ("gpu", "vulkan"):
                    raise RuntimeError(
                        f"[ZeroSilentFallback] Failed to initialize Vulkan GPU for WhisperEngine: {exc}"
                    ) from exc
                logger.warning("Vulkan initialization failed in auto mode, falling back to CPU: %s", exc)
                self.ctx = None

        # Lazy-import to avoid circular deps at module load time
        try:
            from termux_stt.platform.hardware import get_optimal_threads
            self.threads = config.threads or get_optimal_threads()
        except Exception:
            self.threads = config.threads or 4

    # ------------------------------------------------------------------
    # Binary location
    # ------------------------------------------------------------------

    def _get_binary_path(self) -> str:
        """Locate the ``whisper.cpp`` binary (whisper-cli or whisper-cpp)."""
        import shutil
        searched_paths = []
        for name in ["whisper-cli", "whisper-cpp", "main"]:
            found = shutil.which(name)
            if found and (os.access(found, os.X_OK) or os.name == "nt"):
                return found
            searched_paths.append(f"PATH:{name}")

        prefix = os.environ.get("PREFIX", "/data/data/com.termux/files/usr")
        bundled_bin = Path(__file__).resolve().parent.parent / "bin" / "whisper-cli"
        candidates = [
            bundled_bin,
            Path(prefix) / "bin" / "whisper-cli",
            Path(prefix) / "bin" / "whisper-cpp",
            Path.home() / ".local" / "bin" / "whisper-cli",
            Path.home() / ".local" / "bin" / "whisper-cpp",
            Path("/data/data/com.termux/files/home/.local/bin/whisper-cli"),
            Path("/data/data/com.termux/files/home/.local/bin/whisper-cpp"),
            Path("/usr/local/bin/whisper-cli"),
            Path("/usr/local/bin/whisper-cpp"),
        ]
        for p in candidates:
            searched_paths.append(str(p))
            if p.exists() and (os.access(str(p), os.X_OK) or os.name == "nt"):
                return str(p)

        # Raise informative error if not found in any candidate path
        searched_fmt = "\n  - ".join(searched_paths)
        raise FileNotFoundError(
            f"Cannot locate 'whisper.cpp' runtime executable (whisper-cli or whisper-cpp).\n"
            f"Searched candidate locations:\n  - {searched_fmt}\n\n"
            f"Action Required:\n"
            f"  1. Run automatic installer: termux-stt install\n"
            f"  2. Or install manually via Termux: pkg install whisper.cpp\n"
            f"  3. Or compile whisper.cpp and add to PATH: export PATH=$HOME/.local/bin:$PATH"
        )

    @classmethod
    def _supports_gpu(cls, binary_path: str) -> dict:
        """Inspects whether the target whisper-cli binary supports GPU offload flags (-ngl, -dev, -ng)."""
        if not hasattr(cls, "_gpu_flags_cache"):
            cls._gpu_flags_cache = {}
        if binary_path in cls._gpu_flags_cache:
            return cls._gpu_flags_cache[binary_path]
        try:
            res = run_isolated([binary_path, "-h"])
            help_text = (res.stdout or "") + (res.stderr or "")
            flags = {
                "ngl": "-ngl" in help_text or "--gpu-layers" in help_text,
                "dev": "-dev" in help_text or "--device" in help_text,
                "no_gpu": "-ng" in help_text or "--no-gpu" in help_text,
            }
            flags["supports_gpu"] = flags["ngl"] or flags["dev"] or flags["no_gpu"]
            cls._gpu_flags_cache[binary_path] = flags
            return flags
        except Exception:
            flags = {"ngl": False, "dev": False, "no_gpu": False, "supports_gpu": False}
            cls._gpu_flags_cache[binary_path] = flags
            return flags

    @classmethod
    def _supports_ngl(cls, binary_path: str) -> bool:
        """Inspects whether the target whisper-cli binary supports GPU offload flags (-ngl or -dev)."""
        return cls._supports_gpu(binary_path)["supports_gpu"]


    # ------------------------------------------------------------------
    # JSON parsing
    # ------------------------------------------------------------------

    def _parse_whisper_json(self, json_str: str) -> List[Segment]:
        """Parse ``whisper.cpp --output-json`` output into Segment list."""
        segments: List[Segment] = []
        try:
            data = json.loads(json_str)
            for seg in data.get("transcription", []):
                offsets = seg.get("offsets", {})
                if isinstance(offsets, dict):
                    t0 = offsets.get("from", 0) / 1000.0
                    t1 = offsets.get("to", 0) / 1000.0
                else:
                    t0, t1 = 0.0, 0.0
                text = seg.get("text", "").strip()
                if text:
                    segments.append(Segment(start=t0, end=t1, text=text))
        except Exception as exc:
            logger.error("Failed to parse whisper.cpp JSON output: %s", exc)
        return segments

    # ------------------------------------------------------------------
    # Core engine methods
    # ------------------------------------------------------------------

    def transcribe(self, audio_path: str, **kwargs: Any) -> TranscriptResult:
        """Transcribe an audio file using whisper.cpp."""
        from termux_stt.audio.preprocessor import preprocess
        from termux_stt.models.hub import ModelHub
        from termux_stt.platform.hardware import is_termux
        from termux_stt.platform.process_pool import run_isolated

        # 1. Preprocess to 16 kHz mono WAV
        wav_path = preprocess(audio_path, target_sr=16000, force_mono=True)
        is_temp_wav = os.path.abspath(wav_path) != os.path.abspath(audio_path)

        try:
            # 2. Ensure model is downloaded
            model_path = ModelHub.ensure_model('whisper', self.model)

            # 3. Build command with all whisper.cpp control flags
            binary = self._get_binary_path()
            cmd = [
                binary,
                "-m", model_path,
                "-l", self.lang,
                "-t", str(self.threads),
                "-oj",  # output JSON
                "-f", wav_path,
            ]

            # Extract options from kwargs or self.config.extra
            opts = {**self.config.extra, **kwargs}

            if "prompt" in opts or "initial_prompt" in opts:
                prompt_val = opts.get("prompt") or opts.get("initial_prompt")
                cmd.extend(["--prompt", str(prompt_val)])
            if "beam_size" in opts:
                cmd.extend(["-bs", str(opts["beam_size"])])
            if "best_of" in opts:
                cmd.extend(["-bo", str(opts["best_of"])])
            if "temperature" in opts:
                cmd.extend(["-tp", str(opts["temperature"])])
            if opts.get("translate", False):
                cmd.append("-tr")
            if "max_len" in opts:
                cmd.extend(["-ml", str(opts["max_len"])])
            if opts.get("split_on_word", False):
                cmd.append("-sow")
            # Default to no_fallback on Termux unless explicitly disabled
            if opts.get("no_fallback", is_termux()):
                cmd.append("-nf")
            if "suppress_regex" in opts:
                cmd.extend(["--suppress-regex", str(opts["suppress_regex"])])
            if "grammar" in opts:
                cmd.extend(["--grammar", str(opts["grammar"])])
            if opts.get("dtw", False):
                cmd.append("-dtw")

            # GPU offloading via Vulkan if active and supported by binary
            dev_lower = str(self.device or "auto").strip().lower()
            is_gpu_req = (
                dev_lower in ("gpu", "vulkan")
                or (self.ctx and getattr(self.ctx, "is_gpu", False))
                or opts.get("gpu_layers")
                or opts.get("n_gpu_layers")
            )
            if is_gpu_req:
                ngl = opts.get("gpu_layers", opts.get("n_gpu_layers", 33))
                gpu_flags = self._supports_gpu(binary)
                if gpu_flags["ngl"]:
                    cmd.extend(["-ngl", str(ngl)])
                elif gpu_flags["dev"]:
                    dev_id = str(opts.get("gpu_device", 0))
                    cmd.extend(["-dev", dev_id])
                elif gpu_flags["supports_gpu"]:
                    pass
                else:
                    if dev_lower in ("gpu", "vulkan"):
                        raise RuntimeError(
                            f"[ZeroSilentFallback] Explicit Vulkan GPU mode requested ('{self.device}'), "
                            f"but whisper-cli binary at '{binary}' does not support GPU offload (-ngl). "
                            f"CPU fallback is strictly forbidden under Zero-Silent-Fallback protocol."
                        )
                    logger.info("whisper-cli at '%s' does not accept GPU flags; running in native CPU mode.", binary)

            # Passthrough raw extra_args if provided (list or string)
            extra_args = opts.get("extra_args")
            if extra_args:
                if isinstance(extra_args, list):
                    cmd.extend(extra_args)
                elif isinstance(extra_args, str):
                    import shlex
                    cmd.extend(shlex.split(extra_args))

            # Golden Link Order LD_LIBRARY_PATH resolution for Vulkan
            vulkan_env = None
            try:
                from ameva_runtime.vulkan.adapters.base import get_vulkan_env
                vulkan_env = get_vulkan_env()
            except ImportError:
                if os.path.exists("/system/lib64/libvulkan.so"):
                    vulkan_env = dict(os.environ)
                    existing_lp = vulkan_env.get("LD_LIBRARY_PATH", "")
                    if "/system/lib64" not in existing_lp:
                        vulkan_env["LD_LIBRARY_PATH"] = f"/system/lib64:{existing_lp}".rstrip(":")

            logger.info("Running whisper.cpp: %s", " ".join(cmd))
            result = run_isolated(cmd, env=vulkan_env)

            if result.returncode != 0:
                raise RuntimeError(
                    f"whisper.cpp exited with code {result.returncode}: "
                    f"{result.stderr}"
                )

            # Verification of Vulkan backend in GPU mode
            if dev_lower in ("gpu", "vulkan"):
                stderr_text = result.stderr or ""
                if "failed to initialize" in stderr_text.lower() or "vk_error" in stderr_text.lower():
                    raise RuntimeError(
                        f"[ZeroSilentFallback] Vulkan backend reported failure during execution:\n{stderr_text}"
                    )

            # 4. Parse JSON result (written to <wav>.json)
            json_file = f"{wav_path}.json"
            segments: List[Segment] = []
            full_text = ""

            if os.path.exists(json_file):
                with open(json_file, "r", encoding="utf-8") as fh:
                    segments = self._parse_whisper_json(fh.read())
                full_text = " ".join(s.text for s in segments)
                try:
                    os.remove(json_file)
                except OSError as _tmp_del_err:
                    import logging; logging.getLogger(__name__).debug("temp file cleanup OSError: %s", _tmp_del_err)

            # Fallback: parse stdout directly if JSON was missing or empty
            if not segments and result.stdout:
                import re
                pattern = re.compile(r"\[(\d{2}):(\d{2}):([\d\.]+)\s*-->\s*(\d{2}):(\d{2}):([\d\.]+)\]\s*(.*)")
                for line in result.stdout.splitlines():
                    m = pattern.search(line)
                    if m:
                        h1, m1, s1, h2, m2, s2, txt = m.groups()
                        t0 = int(h1) * 3600 + int(m1) * 60 + float(s1)
                        t1 = int(h2) * 3600 + int(m2) * 60 + float(s2)
                        txt = txt.strip()
                        if txt:
                            segments.append(Segment(start=t0, end=t1, text=txt))
                if segments:
                    full_text = " ".join(s.text for s in segments)
                elif result.stdout.strip():
                    full_text = result.stdout.strip()
                    segments = [Segment(start=0.0, end=0.0, text=full_text)]

            return TranscriptResult(
                text=full_text,
                language=self.lang,
                segments=segments,
            )
        finally:
            json_file = f"{wav_path}.json"
            if os.path.exists(json_file):
                try:
                    os.remove(json_file)
                except OSError as _tmp_del_err:
                    import logging; logging.getLogger(__name__).debug("temp file cleanup OSError: %s", _tmp_del_err)
            if is_temp_wav and os.path.exists(wav_path):
                try:
                    os.remove(wav_path)
                except OSError as _tmp_del_err:
                    import logging; logging.getLogger(__name__).debug("temp file cleanup OSError: %s", _tmp_del_err)

    def stream_mic(
        self, duration: Optional[float] = None
    ) -> Iterator[Segment]:
        """Stream transcription from the device microphone.

        Records audio in chunks via ``termux-microphone-record``, runs
        VAD to detect speech boundaries, and transcribes each utterance
        with whisper.cpp.
        """
        import tempfile

        from termux_stt.audio.mic import MicCapture

        mic = MicCapture()
        chunk_sec = 5.0  # seconds per chunk

        for chunk_bytes in mic.stream(duration=duration, chunk_sec=chunk_sec):
            # Write chunk to a temp WAV for whisper.cpp
            with tempfile.NamedTemporaryFile(
                suffix=".wav", delete=False
            ) as tmp:
                tmp_path = tmp.name
                # Write a minimal WAV header + PCM data
                self._write_wav(tmp, chunk_bytes, sample_rate=16000)

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
        import tempfile
        import wave

        from termux_stt.audio.preprocessor import preprocess

        wav_path = preprocess(audio_path, target_sr=16000, force_mono=True)
        with wave.open(wav_path, "rb") as wf:
            chunk_frames = int(chunk_sec * wf.getframerate())
            offset = 0.0
            while True:
                data = wf.readframes(chunk_frames)
                if len(data) == 0:
                    break

                with tempfile.NamedTemporaryFile(
                    suffix=".wav", delete=False
                ) as tmp:
                    tmp_path = tmp.name
                    self._write_wav(tmp, data, sample_rate=wf.getframerate())

                try:
                    result = self.transcribe(tmp_path)
                    for seg in result.segments:
                        yield Segment(
                            start=offset + seg.start,
                            end=offset + seg.end,
                            text=seg.text,
                            speaker=seg.speaker,
                            confidence=seg.confidence,
                        )
                finally:
                    try:
                        os.unlink(tmp_path)
                    except OSError as _tmp_del_err:
                        import logging; logging.getLogger(__name__).debug("temp file cleanup OSError: %s", _tmp_del_err)

                actual_frames = len(data) // (wf.getsampwidth() * wf.getnchannels())
                offset += actual_frames / wf.getframerate()

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
        info = {
            "name": "whisper.cpp",
            "model": self.model,
            "language": self.lang,
            "device": str(self.device),
            "threads": self.threads,
            "binary_path": self._get_binary_path(),
            "quantization": self.config.quantization,
        }
        if self.ctx:
            info["backend_type"] = self.ctx.backend_type
            info["is_gpu"] = self.ctx.is_gpu
            info["device_name"] = self.ctx.device_name
        return info

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _write_wav(fh, pcm_data: bytes, sample_rate: int = 16000) -> None:
        """Write raw PCM s16le data as a WAV file."""
        import struct

        num_channels = 1
        sample_width = 2  # 16-bit
        data_size = len(pcm_data)
        header_size = 44

        fh.write(b"RIFF")
        fh.write(struct.pack("<I", data_size + header_size - 8))
        fh.write(b"WAVE")
        fh.write(b"fmt ")
        fh.write(struct.pack("<I", 16))  # chunk size
        fh.write(struct.pack("<H", 1))   # PCM format
        fh.write(struct.pack("<H", num_channels))
        fh.write(struct.pack("<I", sample_rate))
        fh.write(struct.pack("<I", sample_rate * num_channels * sample_width))
        fh.write(struct.pack("<H", num_channels * sample_width))
        fh.write(struct.pack("<H", sample_width * 8))
        fh.write(b"data")
        fh.write(struct.pack("<I", data_size))
        fh.write(pcm_data)
