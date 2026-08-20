import platform
import shutil
import sys

def run_doctor(args):
    print("System Environment Check:")
    print("-" * 30)
    
    # Check OS
    system = platform.system()
    machine = platform.machine()
    print(f"OS: {system} ({machine})")
    
    # Check FFmpeg
    has_ffmpeg = shutil.which("ffmpeg") is not None
    if has_ffmpeg:
        print("✅ ffmpeg is installed")
    else:
        print("❌ ffmpeg is missing (Required for audio preprocessing)")
        
    # Check Engine Executables (Placeholders for actual checks)
    has_whisper_cpp = shutil.which("whisper-cli") is not None or shutil.which("main") is not None
    if has_whisper_cpp:
        print("✅ whisper.cpp engine found")
    else:
        print("⚠️ whisper.cpp engine missing or not in PATH")
        
    # Python Version
    py_version = sys.version_info
    if py_version >= (3, 8):
        print(f"✅ Python {py_version.major}.{py_version.minor}")
    else:
        print(f"❌ Python version too old: {py_version.major}.{py_version.minor} (Requires >= 3.8)")
        
    print("-" * 30)
    print("Doctor check complete.")
