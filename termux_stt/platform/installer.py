"""
Installer for C++ engines and native dependencies.
"""

import logging
import subprocess
from pathlib import Path
from typing import Dict

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).parent.parent.parent
SCRIPTS_DIR = PROJECT_ROOT / "scripts"


class EngineInstaller:
    """Installer for C++ engines."""

    @classmethod
    def install_whisper_cpp(cls) -> bool:
        """Install whisper.cpp optimized for ARM NEON."""
        logger.info("Installing whisper.cpp...")
        script = SCRIPTS_DIR / "install_whisper_cpp.sh"
        if not script.exists():
            # Fallback inline or search in package
            script = Path("/data/data/com.termux/files/home/termux-stt/scripts/install_whisper_cpp.sh")
        if script.exists():
            result = subprocess.run(["bash", str(script)], capture_output=True)
            return result.returncode == 0
        return False

    @classmethod
    def install_vosk(cls) -> bool:
        """Install Vosk and extract libvosk.so."""
        logger.info("Installing Vosk...")
        script = SCRIPTS_DIR / "install_vosk.sh"
        if not script.exists():
            script = Path("/data/data/com.termux/files/home/termux-stt/scripts/install_vosk.sh")
        if script.exists():
            result = subprocess.run(["bash", str(script)], capture_output=True)
            return result.returncode == 0
        return False

    @classmethod
    def install_sherpa_onnx(cls) -> bool:
        """Install sherpa-onnx for aarch64."""
        logger.info("Installing sherpa-onnx...")
        script = SCRIPTS_DIR / "install_sherpa_onnx.sh"
        if not script.exists():
            script = Path("/data/data/com.termux/files/home/termux-stt/scripts/install_sherpa_onnx.sh")
        if script.exists():
            result = subprocess.run(["bash", str(script)], capture_output=True)
            return result.returncode == 0
        return False

    @classmethod
    def check_engine_installed(cls, engine: str) -> bool:
        """Check if an engine is installed."""
        bin_dir = Path.home() / ".local" / "bin"
        if engine == "whisper":
            return (bin_dir / "whisper-cpp").exists() or (bin_dir / "main").exists()
        elif engine == "vosk":
            return (bin_dir / "libvosk.so").exists() or (Path.home() / ".vosk" / "libvosk.so").exists()
        elif engine == "sherpa":
            return (bin_dir / "sherpa-onnx-offline").exists()
        return False

    @classmethod
    def install_all(cls) -> Dict[str, bool]:
        """Install all engines and return status dict."""
        return {
            "whisper": cls.install_whisper_cpp(),
            "vosk": cls.install_vosk(),
            "sherpa": cls.install_sherpa_onnx()
        }


def main():
    """CLI entrypoint for termux-stt-install."""
    print("=== termux-stt Engine & Model Installer ===")
    print("Setting up on-device STT engines for Termux...")

    results = EngineInstaller.install_all()
    for engine, ok in results.items():
        status = "[OK]" if ok else "[SKIPPED/FAILED]"
        print(f" - {engine}: {status}")

    print("Setup complete. Run 'termux-stt doctor' to verify.")


if __name__ == "__main__":
    main()
