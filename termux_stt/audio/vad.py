"""
Voice Activity Detection (VAD) module.
Provides Silero-VAD and EnergyVAD fallback.
"""

import math
import os
import struct
import subprocess
import tempfile
import wave
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Tuple

__all__ = ["VADResult", "BaseVAD", "SileroVAD", "EnergyVAD", "detect_speech", "split_by_speech"]

@dataclass
class VADResult:
    segments: List[Tuple[float, float]]
    speech_ratio: float

class BaseVAD(ABC):
    @abstractmethod
    def process(self, audio_path: str, threshold: float = 0.5, min_speech_ms: int = 250, min_silence_ms: int = 100) -> VADResult:
        pass

class EnergyVAD(BaseVAD):
    def process(self, audio_path: str, threshold: float = 0.5, min_speech_ms: int = 250, min_silence_ms: int = 100) -> VADResult:
        """Simple pure Python energy-based VAD as fallback."""
        with wave.open(audio_path, 'rb') as wf:
            framerate = wf.getframerate()
            nframes = wf.getnframes()
            audio_data = wf.readframes(nframes)

            samples = struct.unpack(f"<{nframes}h", audio_data)

        # Simplified framing and energy thresholding
        frame_ms = 30
        frame_size = int(framerate * frame_ms / 1000)

        segments = []
        in_speech = False
        start_time = 0.0

        for i in range(0, len(samples), frame_size):
            frame = samples[i:i+frame_size]
            if not frame:
                break

            energy = sum(x*x for x in frame) / len(frame)
            rms = math.sqrt(energy) if energy > 0 else 0

            current_time = i / framerate
            # Heuristic threshold
            if rms > threshold * 1000:
                if not in_speech:
                    in_speech = True
                    start_time = current_time
            else:
                if in_speech:
                    in_speech = False
                    end_time = current_time
                    if (end_time - start_time) * 1000 >= min_speech_ms:
                        segments.append((start_time, end_time))

        total_duration = nframes / framerate
        speech_duration = sum(e - s for s, e in segments)
        speech_ratio = speech_duration / total_duration if total_duration > 0 else 0.0

        return VADResult(segments=segments, speech_ratio=speech_ratio)

class SileroVAD(BaseVAD):
    def process(self, audio_path: str, threshold: float = 0.5, min_speech_ms: int = 250, min_silence_ms: int = 100) -> VADResult:
        """
        Stub for Silero-VAD running via ORT.
        Normally this would invoke a subprocess Python script to keep ORT isolated.
        """
        # For this skeleton, we fallback to EnergyVAD if script is not implemented.
        return EnergyVAD().process(audio_path, threshold, min_speech_ms, min_silence_ms)

def detect_speech(audio_path: str, threshold: float = 0.5, min_speech_ms: int = 250, min_silence_ms: int = 100) -> VADResult:
    """Detect speech segments using available VAD."""
    # Attempt SileroVAD, fallback to EnergyVAD
    vad = EnergyVAD()  # Using Energy fallback as default in this iteration
    return vad.process(audio_path, threshold, min_speech_ms, min_silence_ms)

def split_by_speech(audio_path: str, vad_result: VADResult) -> List[str]:
    """Split audio into temporary files based on VAD segments."""
    output_files = []
    for idx, (start, end) in enumerate(vad_result.segments):
        fd, out_path = tempfile.mkstemp(suffix=f"_seg_{idx}.wav", prefix="vad_")
        os.close(fd)

        cmd = [
            "ffmpeg",
            "-y",
            "-i", audio_path,
            "-ss", str(start),
            "-to", str(end),
            "-c", "copy",
            "-v", "quiet",
            out_path
        ]
        subprocess.run(cmd, check=True)
        output_files.append(out_path)
    return output_files
