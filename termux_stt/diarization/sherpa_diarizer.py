"""
Sherpa-ONNX Native Speaker Diarization Engine.

Leverages PyAnnote Segmentation 3.0 and 3D-Speaker CAM++ embedding models
via sherpa-onnx-offline-speaker-diarization C++ NDK binary.
"""

import logging
import os
import re
import shutil
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from termux_stt.audio.preprocessor import preprocess
from termux_stt.export.result import DiarizedResult, Segment
from termux_stt.models.hub import ModelHub
from termux_stt.platform.process_pool import run_isolated

logger = logging.getLogger(__name__)

__all__ = ["SherpaDiarizer"]


class SherpaDiarizer:
    """High-accuracy on-device neural speaker diarization via Sherpa-ONNX.

    Uses:
      - PyAnnote 3.0 ONNX model for overlap-aware speech segmentation
      - 3D-Speaker CAM++ ONNX model for 192-dim speaker embeddings
      - Fast spectral/agglomerative clustering on-device
    """

    def __init__(
        self,
        segmentation_model: str = "pyannote-segmentation-3-0",
        embedding_model: str = "3dspeaker-campplus",
        num_speakers: Optional[int] = None,
        threshold: float = 0.65,
        provider: str = "cpu",
    ) -> None:
        self.segmentation_model_name = segmentation_model
        self.embedding_model_name = embedding_model
        self.num_speakers = num_speakers
        self.threshold = threshold
        self.provider = provider

    @staticmethod
    def _find_binary(name: str = "sherpa-onnx-offline-speaker-diarization") -> str:
        """Locate sherpa-onnx-offline-speaker-diarization executable."""
        found = shutil.which(name)
        if found:
            return found
        candidates = [
            Path.home() / ".local" / "bin" / name,
            Path(f"/data/data/com.termux/files/home/.local/bin/{name}"),
            Path(f"/data/data/com.termux/files/usr/bin/{name}"),
            Path(f"/data/data/com.termux/files/usr/local/bin/{name}"),
        ]
        for p in candidates:
            if p.exists():
                return str(p)
        raise FileNotFoundError(
            f"Cannot locate '{name}' executable.\n"
            f"Please run 'termux-stt install --engine diarization' or in Python:\n"
            f"  from termux_stt.platform.installer import EngineInstaller\n"
            f"  EngineInstaller.install_diarization()"
        )

    def diarize_audio(
        self, audio_path: str, num_speakers: Optional[int] = None
    ) -> List[Tuple[float, float, int]]:
        """Extract speaker intervals (start_sec, end_sec, speaker_id) from audio.

        Returns
        -------
        List[Tuple[float, float, int]]
            List of (start, end, speaker_id) intervals.
        """
        binary = self._find_binary()
        num_spk = num_speakers if num_speakers is not None else self.num_speakers

        # 1. Preprocess audio to 16kHz mono WAV
        wav_path = preprocess(audio_path, target_sr=16000, force_mono=True)
        is_temp_wav = os.path.abspath(wav_path) != os.path.abspath(audio_path)

        # 2. Ensure models via ModelHub
        seg_dir = ModelHub.ensure_model("sherpa", self.segmentation_model_name)
        emb_path = ModelHub.ensure_model("sherpa", self.embedding_model_name)

        # Robust segmentation ONNX search
        seg_model = None
        search_dirs = [seg_dir]
        if os.path.isfile(seg_dir):
            parent = os.path.dirname(seg_dir)
            search_dirs.extend([
                parent,
                os.path.join(parent, "sherpa-onnx-pyannote-segmentation-3-0"),
                os.path.join(parent, "pyannote-segmentation-3-0"),
            ])
        elif os.path.isdir(seg_dir):
            search_dirs.append(os.path.join(seg_dir, "sherpa-onnx-pyannote-segmentation-3-0"))

        for sd in search_dirs:
            if not sd or not os.path.exists(sd):
                continue
            if os.path.isfile(sd) and sd.endswith(".onnx"):
                seg_model = sd
                break
            for cand in ["model.int8.onnx", "model.onnx"]:
                p = os.path.join(sd, cand)
                if os.path.isfile(p):
                    seg_model = p
                    break
            if seg_model:
                break

        if not seg_model:
            # Fallback recursive search
            base_search = os.path.dirname(seg_dir) if os.path.isfile(seg_dir) else seg_dir
            for root, _, files in os.walk(base_search):
                for f in sorted(files):
                    if f in ("model.int8.onnx", "model.onnx") or (f.endswith(".onnx") and "segment" in f.lower()):
                        seg_model = os.path.join(root, f)
                        break
                if seg_model:
                    break

        if not seg_model:
            raise FileNotFoundError(
                f"Cannot find segmentation .onnx model in or near: {seg_dir}.\n"
                f"Please run 'termux-stt install --engine diarization' or in Python:\n"
                f"  from termux_stt.platform.installer import EngineInstaller\n"
                f"  EngineInstaller.install_diarization()"
            )

        cmd = [
            binary,
            f"--segmentation.pyannote-model={seg_model}",
            f"--embedding.model={emb_path}",
            f"--segmentation.provider={self.provider}",
            f"--embedding.provider={self.provider}",
        ]

        if num_spk and num_spk > 0:
            cmd.append(f"--clustering.num-clusters={num_spk}")
        else:
            cmd.append(f"--clustering.threshold={self.threshold}")

        cmd.append(wav_path)

        logger.info("Executing sherpa speaker diarization: %s", " ".join(cmd))
        try:
            result = run_isolated(cmd)
            if result.returncode != 0:
                raise RuntimeError(
                    f"sherpa-onnx-offline-speaker-diarization failed with exit code {result.returncode}: "
                    f"{result.stderr}"
                )

            return self._parse_output(result.stdout)
        finally:
            if is_temp_wav and os.path.exists(wav_path):
                try:
                    os.remove(wav_path)
                except OSError:
                    pass

    @staticmethod
    def _parse_output(stdout: str) -> List[Tuple[float, float, int]]:
        """Parse sherpa-onnx speaker diarization stdout timestamps.

        Standard output format examples:
          start: 0.120, end: 3.450, speaker: 0
          or
          SPEAKER test 1 0.120 3.330 <NA> <NA> 0 <NA> <NA> (RTTM)
          or
          0.120 -- 3.450: speaker 0
        """
        intervals = []
        for line in stdout.splitlines():
            line = line.strip()
            if not line:
                continue

            # Format 1: start: 0.120, end: 3.450, speaker: 0
            m1 = re.search(r"start\s*:\s*([\d\.]+).*?end\s*:\s*([\d\.]+).*?speaker\s*:\s*(\d+)", line, re.IGNORECASE)
            if m1:
                start = float(m1.group(1))
                end = float(m1.group(2))
                spk = int(m1.group(3))
                intervals.append((start, end, spk))
                continue

            # Format 2: 0.120 -- 3.450: speaker 0 or 0.284 -- 2.107 speaker_00
            m2 = re.search(r"([\d\.]+)\s*(?:--|-|to)\s*([\d\.]+)\s*[:\s]*speaker_?(\d+)", line, re.IGNORECASE)
            if m2:
                start = float(m2.group(1))
                end = float(m2.group(2))
                spk = int(m2.group(3))
                intervals.append((start, end, spk))
                continue

            # Format 3: RTTM standard: SPEAKER <file> <channel> <start> <duration> <NA> <NA> <spk>
            parts = line.split()
            if len(parts) >= 8 and parts[0].upper() == "SPEAKER":
                try:
                    start = float(parts[3])
                    dur = float(parts[4])
                    spk_str = parts[7]
                    spk_id = int(re.sub(r"\D", "", spk_str)) if any(c.isdigit() for c in spk_str) else 0
                    intervals.append((start, start + dur, spk_id))
                except (ValueError, IndexError):
                    continue

        intervals.sort(key=lambda x: x[0])
        return intervals
