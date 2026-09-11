"""
System doctor and environment diagnostic command.
"""

import platform
import shutil
import sys


def _status_tag(status: str) -> str:
    """Return status tag safely handling terminal encoding."""
    # Check if terminal supports unicode
    encoding = getattr(sys.stdout, 'encoding', 'utf-8') or 'utf-8'
    try:
        '\u2705'.encode(encoding)
        can_unicode = True
    except (UnicodeEncodeError, LookupError):
        can_unicode = False

    if can_unicode:
        if status == 'ok':
            return "✅ [OK]"
        elif status == 'warn':
            return "⚠️  [WARN]"
        else:
            return "❌ [FAIL]"
    else:
        if status == 'ok':
            return "[OK]"
        elif status == 'warn':
            return "[WARN]"
        else:
            return "[FAIL]"


def run_doctor(args):
    print("System Environment Check:")
    print("-" * 35)

    # Check OS
    system = platform.system()
    machine = platform.machine()
    print(f"OS: {system} ({machine})")

    # Check FFmpeg
    has_ffmpeg = shutil.which("ffmpeg") is not None
    if has_ffmpeg:
        print(f"{_status_tag('ok')} ffmpeg is installed")
    else:
        print(f"{_status_tag('fail')} ffmpeg is missing (Required for audio preprocessing)")

    # Check Engine Executables
    has_whisper_cpp = (
        shutil.which("whisper-cpp") is not None
        or shutil.which("whisper-cli") is not None
        or shutil.which("main") is not None
    )
    if has_whisper_cpp:
        print(f"{_status_tag('ok')} whisper.cpp engine found")
    else:
        print(f"{_status_tag('warn')} whisper.cpp engine missing or not in PATH")

    # Check Vosk
    try:
        import vosk  # noqa: F401
        print(f"{_status_tag('ok')} vosk Python binding is installed")
    except ImportError:
        print(f"{_status_tag('warn')} vosk is missing (Install via: pip install vosk)")

    # Check Sherpa ONNX
    has_sherpa = shutil.which("sherpa-onnx-offline") is not None
    if has_sherpa:
        print(f"{_status_tag('ok')} sherpa-onnx binary found")
    else:
        print(f"{_status_tag('warn')} sherpa-onnx-offline missing or not in PATH")

    # Check Microphone capture tools
    has_mic_tool = shutil.which("termux-microphone-record") is not None or shutil.which("ffmpeg") is not None
    if has_mic_tool:
        print(f"{_status_tag('ok')} microphone capture tool available")
    else:
        print(f"{_status_tag('warn')} no microphone tool found (termux-api or ffmpeg required)")

    # Python Version
    py_version = sys.version_info
    if py_version >= (3, 8):
        print(f"{_status_tag('ok')} Python {py_version.major}.{py_version.minor}.{py_version.micro}")
    else:
        print(f"{_status_tag('fail')} Python version too old: {py_version.major}.{py_version.minor} (Requires >= 3.8)")

    print("-" * 35)
    print("Doctor check complete.")
