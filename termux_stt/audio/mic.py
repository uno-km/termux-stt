"""
Microphone capture for Termux using termux-api.
"""

import os
import subprocess
from typing import Optional, Iterator

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

    def stream(self) -> Iterator[bytes]:
        """Stream 16kHz PCM chunks from mic."""
        raise NotImplementedError("Streaming directly from termux-microphone is not fully supported yet.")
