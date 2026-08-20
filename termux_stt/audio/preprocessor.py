"""
Audio preprocessor for termux-stt.
Converts any input audio to 16kHz Mono PCM WAV using ffmpeg.
"""

import os
import tempfile
import subprocess
from typing import Optional

__all__ = ["preprocess", "ensure_wav_format", "validate_audio"]


def validate_audio(path: str) -> bool:
    """
    Validate audio size and length.
    Ensure it's not totally empty or impossibly small.
    """
    if not os.path.exists(path):
        return False
    size = os.path.getsize(path)
    if size < 44:  # At least smaller than a wav header
        return False
    return True


def preprocess(
    input_path: str,
    output_path: Optional[str] = None,
    target_sr: int = 16000,
    force_mono: bool = True,
) -> str:
    """
    Convert audio to 16kHz, 1 channel, PCM s16le WAV.
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")

    # If the file is already a valid 16kHz mono WAV and no specific output_path requested,
    # we can use ensure_wav_format or convert to a safe temp WAV
    if output_path is None:
        fd, output_path = tempfile.mkstemp(suffix=".wav", prefix="termux_stt_")
        os.close(fd)

    channels = "1" if force_mono else "2"
    cmd = [
        "ffmpeg",
        "-y",
        "-i", input_path,
        "-ac", channels,
        "-ar", str(target_sr),
        "-c:a", "pcm_s16le",
        "-v", "quiet",
        output_path
    ]

    try:
        subprocess.run(cmd, check=True)
        return output_path
    except subprocess.CalledProcessError as e:
        if os.path.exists(output_path):
            os.remove(output_path)
        raise RuntimeError(f"FFmpeg conversion failed: {e}")


def ensure_wav_format(path: str) -> str:
    """
    Check if the file is already 16kHz mono pcm_s16le wav.
    If not, convert it and return the new temp path.
    """
    cmd = [
        "ffprobe",
        "-v", "quiet",
        "-print_format", "json",
        "-show_streams",
        path
    ]
    try:
        import json
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        info = json.loads(result.stdout)
        streams = info.get("streams", [])
        if streams:
            stream = streams[0]
            if (stream.get("codec_name") == "pcm_s16le" and 
                stream.get("channels") == 1 and 
                str(stream.get("sample_rate")) == "16000"):
                return path
    except Exception:
        pass  # fallback to preprocess
    
    return preprocess(path)
