"""
Microphone capture for Termux using termux-api.
"""

import subprocess
from typing import Iterator, Optional

__all__ = ["MicCapture"]

class MicCapture:
    """Capture audio from microphone in Termux."""

    def __init__(self):
        self._output_path: Optional[str] = None
        self._is_recording = False

    def start_recording(self, output_path: str, duration: Optional[float] = None, sample_rate: int = 16000) -> None:
        """Start recording using termux-microphone-record."""
        if self._is_recording:
            raise RuntimeError("Already recording.")

        self._output_path = output_path
        cmd = ["termux-microphone-record", "-f", output_path]
        if duration:
            cmd.extend(["-l", str(int(duration))])

        subprocess.run(cmd, check=True)
        self._is_recording = True

    def stop_recording(self) -> None:
        """Stop current recording."""
        if not self._is_recording:
            return

        subprocess.run(["termux-microphone-record", "-q"], check=True)
        self._is_recording = False
        self._output_path = None

    def stream(self, duration: Optional[float] = None, chunk_sec: float = 2.0, sample_rate: int = 16000) -> Iterator[bytes]:
        """Stream 16kHz PCM chunks from mic."""
        import os
        import shutil
        import tempfile
        import time
        import wave

        start_time = time.time()

        # Method A: FFmpeg or ALSA/Pulse/Direct pipe capture if available
        if shutil.which("ffmpeg"):
            # Try recording pipe or short rolling temporary chunks
            pass

        # Method B: Robust chunk-based capture for Termux termux-microphone-record
        while True:
            if duration is not None and (time.time() - start_time) >= duration:
                break

            with tempfile.NamedTemporaryFile(suffix=".wav", prefix="termux_mic_", delete=False) as tmp:
                tmp_path = tmp.name

            try:
                # Record a chunk
                actual_duration = min(chunk_sec, max(0.5, duration - (time.time() - start_time))) if duration else chunk_sec
                if shutil.which("termux-microphone-record"):
                    subprocess.run(["termux-microphone-record", "-f", tmp_path, "-l", str(max(1, int(actual_duration)))], check=False, capture_output=True)
                    time.sleep(actual_duration)
                    subprocess.run(["termux-microphone-record", "-q"], check=False, capture_output=True)
                elif shutil.which("ffmpeg"):
                    # Record a short snippet via ffmpeg default audio source
                    cmd = ["ffmpeg", "-y", "-t", str(actual_duration), "-ar", str(sample_rate), "-ac", "1", "-c:a", "pcm_s16le", tmp_path]
                    subprocess.run(cmd, check=False, capture_output=True)

                if os.path.exists(tmp_path) and os.path.getsize(tmp_path) > 44:
                    try:
                        with wave.open(tmp_path, "rb") as wf:
                            pcm_data = wf.readframes(wf.getnframes())
                            if pcm_data:
                                yield pcm_data
                    except Exception as wave_err:
                        raise RuntimeError(f"Failed to read recorded microphone WAV: {wave_err}") from wave_err
                else:
                    raise RuntimeError(
                        "Microphone capture failed to record audio data. "
                        "Ensure microphone permissions are granted and recording utilities "
                        "(termux-api package with termux-microphone-record or ffmpeg) are properly installed."
                    )
            finally:
                if os.path.exists(tmp_path):
                    try:
                        os.remove(tmp_path)
                    except OSError:
                        pass
