"""Sherpa-ONNX engine wrapper ??ONNX Runtime based STT for Termux.

Supports Zipformer streaming/offline models, SenseVoice, and CAM++
speaker embedding extraction.
"""

import logging
import os
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional, Tuple

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

    def _build_transcribe_cmd(self, binary: str, model_dir: str, wav_path: str) -> List[str]:
        """Build command line arguments dynamically based on model architecture."""
        cmd = [binary]
        provider = self.config.extra.get('provider', getattr(self.config, 'device', 'cpu'))
        if provider in ('opencl', 'gpu', 'mali', 'adreno'):
            # sherpa-onnx supports cpu, cuda, coreml; fallback to cpu with max threads
            provider = 'cpu'
        cmd.append(f"--provider={provider}")

        # Check for SenseVoice model architecture
        sensevoice_candidates = [
            os.path.join(model_dir, "model.int8.onnx"),
            os.path.join(model_dir, "model.onnx"),
        ]
        sensevoice_model = next((p for p in sensevoice_candidates if os.path.exists(p)), None)
        tokens_path = os.path.join(model_dir, "tokens.txt")

        if sensevoice_model and os.path.exists(tokens_path):
            threads = self.config.threads or 4
            cmd.extend([
                f"--num-threads={threads}",
                f"--sense-voice-model={sensevoice_model}",
                f"--tokens={tokens_path}",
                f"--sense-voice-language={self.config.language}",
                "--sense-voice-use-itn=true",
            ])
            cmd.append(wav_path)
            return cmd

        # Check for Zipformer / Transducer architecture
        encoder_path = os.path.join(model_dir, "encoder.onnx")
        decoder_path = os.path.join(model_dir, "decoder.onnx")
        joiner_path = os.path.join(model_dir, "joiner.onnx")

        if os.path.exists(encoder_path) and os.path.exists(tokens_path):
            cmd.extend([
                f"--tokens={tokens_path}",
                f"--encoder={encoder_path}",
            ])
            if os.path.exists(decoder_path):
                cmd.append(f"--decoder={decoder_path}")
            if os.path.exists(joiner_path):
                cmd.append(f"--joiner={joiner_path}")
            cmd.append(wav_path)
            return cmd

        # Fallback generic directory search
        cmd.extend([
            f"--tokens={tokens_path}",
            f"--encoder={encoder_path}",
            f"--decoder={decoder_path}",
            f"--joiner={joiner_path}",
            wav_path,
        ])
        return cmd

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

        cmd = self._build_transcribe_cmd(binary, model_dir, wav_path)

        try:
            result = run_isolated(cmd)
            if result.returncode != 0:
                raise RuntimeError(
                    f"sherpa-onnx exited with code {result.returncode}: "
                    f"{result.stderr}"
                )

            raw_out = result.stdout.strip()
            text = raw_out
            segments = []

            # Compute duration from WAV if available
            import wave
            audio_dur = 0.0
            try:
                with wave.open(wav_path, "rb") as wf:
                    audio_dur = wf.getnframes() / float(wf.getframerate())
            except Exception:
                pass

            # Try parsing structured SenseVoice JSON output
            import json
            for line in raw_out.splitlines():
                line = line.strip()
                if line.startswith("{") and "text" in line:
                    try:
                        data = json.loads(line)
                        if "text" in data:
                            text = data["text"]
                            tokens = data.get("tokens", [])
                            timestamps = data.get("timestamps", [])
                            if tokens and timestamps and len(tokens) == len(timestamps):
                                for i, (tok, ts) in enumerate(zip(tokens, timestamps)):
                                    tok_clean = tok.strip()
                                    # Filter special tags (<|ko|>, <|NEUTRAL|>, <|Speech|>, <|withitn|>)
                                    if tok_clean.startswith("<|") and tok_clean.endswith("|>"):
                                        continue
                                    end_ts = timestamps[i + 1] if i + 1 < len(timestamps) else (ts + 0.3)
                                    segments.append(Segment(start=float(ts), end=float(end_ts), text=tok))
                            break
                    except Exception:
                        pass

            if not segments:
                for line in raw_out.splitlines():
                    line = line.strip()
                    if line and not line.startswith("{") and not line.startswith("Done") and not line.startswith("Started") and not line.startswith("Elapsed") and not line.startswith("Real time") and not line.startswith("num threads"):
                        segments.append(Segment(start=0.0, end=audio_dur, text=line))

            if not segments and text:
                segments = [Segment(start=0.0, end=audio_dur, text=text)]

            return TranscriptResult(
                text=text,
                language=self.config.language,
                segments=segments,
                duration=audio_dur,
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

    @staticmethod
    def _group_speaker_turns(
        speaker_labels: List[Tuple[float, float, int]], max_gap: float = 1.0
    ) -> List[Tuple[float, float, int]]:
        """Group consecutive time intervals of the same speaker into cohesive turns."""
        if not speaker_labels:
            return []
        sorted_labels = sorted(speaker_labels, key=lambda x: x[0])
        turns: List[Tuple[float, float, int]] = []
        curr_s, curr_e, curr_spk = sorted_labels[0]

        for s, e, spk in sorted_labels[1:]:
            if spk == curr_spk and (s - curr_e) <= max_gap:
                curr_e = max(curr_e, e)
            else:
                turns.append((curr_s, curr_e, curr_spk))
                curr_s, curr_e, curr_spk = s, e, spk
        turns.append((curr_s, curr_e, curr_spk))
        return turns

    @staticmethod
    def _slice_wav(src_path: str, dst_path: str, start_sec: float, end_sec: float, pad_sec: float = 0.08) -> bool:
        """Extract a sub-slice from a 16kHz mono WAV file."""
        import wave
        try:
            with wave.open(src_path, "rb") as r:
                sr = r.getframerate()
                sw = r.getsampwidth()
                nc = r.getnchannels()
                total_frames = r.getnframes()
                dur = total_frames / float(sr)

                s = max(0.0, start_sec - pad_sec)
                e = min(dur, end_sec + pad_sec)
                if e <= s:
                    return False

                start_frame = int(s * sr)
                num_frames = int((e - s) * sr)

                r.setpos(start_frame)
                frames = r.readframes(num_frames)

            with wave.open(dst_path, "wb") as w:
                w.setnchannels(nc)
                w.setsampwidth(sw)
                w.setframerate(sr)
                w.writeframes(frames)
            return True
        except Exception as exc:
            logger.debug("Failed to slice wav: %s", exc)
            return False

    def diarize(
        self, audio_path: str, num_speakers: int = 2, **kwargs: Any
    ) -> DiarizedResult:
        """Run STT with state-of-the-art neural speaker diarization.

        1. Extracts neural speaker intervals using SherpaDiarizer (PyAnnote 3.0 + CAM++).
        2. Performs turn-based segmented transcription for multi-speaker dialogues.
        3. Aligns speaker intervals with text segments and merges consecutive utterances.
        """
        import os
        from termux_stt.diarization.mapper import SpeakerMapper
        from termux_stt.diarization.sherpa_diarizer import SherpaDiarizer

        # Step 1: Neural Speaker Diarization
        try:
            diarizer = SherpaDiarizer(
                num_speakers=num_speakers,
                threshold=kwargs.get("threshold", 0.65),
                provider=self.config.extra.get("provider", "cpu"),
            )
            speaker_labels = diarizer.diarize_audio(audio_path, num_speakers=num_speakers)
            logger.info("Neural diarization extracted %d speaker intervals", len(speaker_labels))
        except Exception as diar_exc:
            logger.warning("Native SherpaDiarizer error (%s), fallback to base transcribe", diar_exc)
            speaker_labels = []

        mapper = SpeakerMapper()
        if speaker_labels:
            speaker_labels = mapper._normalize_speaker_ids(speaker_labels)

        # Step 2: Multi-Speaker Turn-based STT or Single-Pass STT
        turns = self._group_speaker_turns(speaker_labels) if speaker_labels else []
        distinct_speakers = {t[2] for t in turns}

        use_turn_slicing = len(turns) >= 2 and (len(distinct_speakers) >= 2 or num_speakers >= 2)

        aligned_segments: List[Segment] = []
        total_text_parts: List[str] = []

        if use_turn_slicing:
            import tempfile
            from termux_stt.audio.preprocessor import preprocess
            wav_path = preprocess(audio_path, target_sr=16000, force_mono=True)
            is_temp_wav = os.path.abspath(wav_path) != os.path.abspath(audio_path)

            try:
                for turn_idx, (t_start, t_end, spk_id) in enumerate(turns):
                    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as slice_tmp:
                        slice_path = slice_tmp.name

                    try:
                        pad = 0.08
                        actual_start = max(0.0, t_start - pad)
                        if self._slice_wav(wav_path, slice_path, t_start, t_end, pad_sec=pad):
                            slice_res = self.transcribe(slice_path, **kwargs)
                            spk_label = mapper.format_speaker_label(spk_id)
                            for s in slice_res.segments:
                                s.start += actual_start
                                s.end += actual_start
                                s.speaker = spk_label
                                aligned_segments.append(s)
                            if slice_res.text:
                                total_text_parts.append(f"[{spk_label}] {slice_res.text.strip()}")
                    finally:
                        if os.path.exists(slice_path):
                            try:
                                os.remove(slice_path)
                            except OSError:
                                pass
            finally:
                if is_temp_wav and os.path.exists(wav_path):
                    try:
                        os.remove(wav_path)
                    except OSError:
                        pass

        # Fallback to single-pass if turn slicing was not used or yielded no segments
        if not aligned_segments:
            trans_res = self.transcribe(audio_path, **kwargs)
            aligned_segments = mapper.align(trans_res.segments, speaker_labels, num_speakers=num_speakers)
            combined_text = trans_res.text
        else:
            combined_text = "\n".join(total_text_parts)

        # Step 3: Align and merge consecutive utterances
        merged_segments = mapper.merge_consecutive(aligned_segments)
        speakers = sorted(list({s.speaker for s in merged_segments if s.speaker}))

        if not combined_text and merged_segments:
            combined_text = "\n".join(f"[{s.speaker}] {s.text}" for s in merged_segments)

        import wave
        audio_dur = 0.0
        try:
            with wave.open(audio_path, "rb") as wf:
                audio_dur = wf.getnframes() / float(wf.getframerate())
        except Exception:
            pass

        return DiarizedResult(
            text=combined_text,
            language=self.config.language,
            segments=merged_segments,
            duration=audio_dur,
            speakers=speakers,
        )

    def get_info(self) -> Dict[str, Any]:
        """Return engine status information."""
        return {
            "name": "Sherpa-ONNX",
            "model": self.model_name,
            "language": self.config.language,
            "binary_path": self._find_binary(),
        }
