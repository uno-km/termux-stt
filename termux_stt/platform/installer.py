"""
1-Click Self-Contained Native Engine & Dependency Installer for Termux.
Provisions ffmpeg, clang, cmake, and builds whisper.cpp with ARM NEON.
"""

import logging
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Dict

logger = logging.getLogger(__name__)

PREFIX = os.environ.get("PREFIX", "/data/data/com.termux/files/usr")
HOME = os.environ.get("HOME", os.path.expanduser("~"))
LOCAL_BIN = Path(HOME) / ".local" / "bin"
PREFIX_BIN = Path(PREFIX) / "bin"


class EngineInstaller:
    """Automated installer for native dependencies and C++ engines."""

    PREBUILT_WHISPER_URLS = [
        "https://github.com/uno-km/termux-stt/releases/download/v1.1.2/whisper-cli-arm64-android",
        "https://github.com/uno-km/termux-stt/releases/download/v1.1.1/whisper-cli-arm64-android",
        "https://github.com/uno-km/termux-stt/releases/download/v1.1.0/whisper-cli-arm64-android",
        "https://github.com/uno-km/termux-stt/releases/download/v1.0.0/whisper-cli-arm64-android",
    ]

    @classmethod
    def install_system_dependencies(cls) -> bool:
        """Install required Termux runtime packages (ffmpeg, libbluray, libxml2, git)."""
        print("[*] Provisioning native system packages (ffmpeg, libbluray, libxml2, git)...")
        if not shutil.which("pkg"):
            logger.warning("'pkg' command not found, skipping system package provisioning.")
            return True

        try:
            cmd = ["pkg", "install", "-y", "ffmpeg", "libbluray", "libxml2", "git", "termux-api", "curl"]
            res = subprocess.run(cmd, check=False)
            return res.returncode == 0
        except Exception as e:
            logger.error(f"Failed to install system packages: {e}")
            return False

    @classmethod
    def _download_prebuilt_whisper(cls) -> bool:
        """Attempt to download precompiled ARM64 Bionic whisper-cli binary."""
        import urllib.request
        LOCAL_BIN.mkdir(parents=True, exist_ok=True)
        target_path = LOCAL_BIN / "whisper-cli"

        print("[*] Attempting 1-second direct download of pre-compiled whisper.cpp ARM64 binary...")
        for url in cls.PREBUILT_WHISPER_URLS:
            try:
                req = urllib.request.Request(
                    url,
                    headers={"User-Agent": "termux-stt-installer/1.1.1 (Android; ARM64)"}
                )
                with urllib.request.urlopen(req, timeout=10) as response, open(target_path, 'wb') as out_file:
                    shutil.copyfileobj(response, out_file)

                # Check if downloaded file is valid executable (>100KB)
                if target_path.exists() and target_path.stat().st_size > 100 * 1024:
                    target_path.chmod(0o755)
                    # Also link/copy to whisper-cpp
                    shutil.copy2(target_path, LOCAL_BIN / "whisper-cpp")
                    (LOCAL_BIN / "whisper-cpp").chmod(0o755)

                    # Copy to PREFIX/bin if writable
                    try:
                        if PREFIX_BIN.exists() and os.access(PREFIX_BIN, os.W_OK):
                            shutil.copy2(target_path, PREFIX_BIN / "whisper-cli")
                            shutil.copy2(target_path, PREFIX_BIN / "whisper-cpp")
                            (PREFIX_BIN / "whisper-cli").chmod(0o755)
                            (PREFIX_BIN / "whisper-cpp").chmod(0o755)
                    except Exception:
                        pass

                    print(f"[+] Pre-compiled whisper.cpp binary successfully installed to {target_path}")
                    return True
                else:
                    if target_path.exists():
                        target_path.unlink()
            except Exception as e:
                logger.debug(f"Prebuilt download attempt failed for {url}: {e}")
                continue

        print("[-] Pre-built binary download unavailable or offline. Falling back to local native compilation...")
        return False

    @classmethod
    def install_whisper_cpp(cls) -> bool:
        """Install whisper.cpp: Priority 1 = Pre-built download, Priority 2 = Local ARM NEON build."""
        LOCAL_BIN.mkdir(parents=True, exist_ok=True)

        # Check if already installed and executable
        if (PREFIX_BIN / "whisper-cli").exists() or (PREFIX_BIN / "whisper-cpp").exists() or (LOCAL_BIN / "whisper-cli").exists() or (LOCAL_BIN / "whisper-cpp").exists():
            print("[+] whisper.cpp binary is already present.")
            return True

        # Priority 1: Fast Direct Pre-built Download
        if cls._download_prebuilt_whisper():
            return True

        # Priority 2: Fallback to Local CMake & Clang compilation
        print("[*] Setting up whisper.cpp native engine via local compiler with ARM NEON...")
        if shutil.which("pkg"):
            subprocess.run(["pkg", "install", "-y", "cmake", "make", "clang"], check=False)

        build_dir = Path(HOME) / "tmp" / "whisper.cpp"
        build_dir.parent.mkdir(parents=True, exist_ok=True)

        try:
            if not build_dir.exists():
                print("[*] Cloning whisper.cpp repository...")
                subprocess.run(
                    ["git", "clone", "--depth", "1", "https://github.com/ggerganov/whisper.cpp.git", str(build_dir)],
                    check=True,
                )

            print("[*] Compiling whisper.cpp with -DBUILD_SHARED_LIBS=OFF -DWHISPER_NEON=ON...")
            nproc = os.cpu_count() or 4
            subprocess.run(
                ["cmake", "-B", "build", "-DBUILD_SHARED_LIBS=OFF", "-DWHISPER_BUILD_SHARED=OFF", "-DWHISPER_NEON=ON", "-DCMAKE_BUILD_TYPE=Release"],
                cwd=str(build_dir),
                check=True,
            )
            subprocess.run(
                ["cmake", "--build", "build", f"-j{nproc}"],
                cwd=str(build_dir),
                check=True,
            )

            # Locate built binary
            bin_source = None
            if (build_dir / "build" / "bin" / "whisper-cli").exists():
                bin_source = build_dir / "build" / "bin" / "whisper-cli"
            elif (build_dir / "build" / "bin" / "main").exists():
                bin_source = build_dir / "build" / "bin" / "main"

            if bin_source and bin_source.exists():
                # Copy to PREFIX/bin if writable, else LOCAL_BIN
                for target_name in ["whisper-cli", "whisper-cpp"]:
                    try:
                        if PREFIX_BIN.exists() and os.access(PREFIX_BIN, os.W_OK):
                            shutil.copy2(bin_source, PREFIX_BIN / target_name)
                            (PREFIX_BIN / target_name).chmod(0o755)
                    except Exception:
                        pass
                    shutil.copy2(bin_source, LOCAL_BIN / target_name)
                    (LOCAL_BIN / target_name).chmod(0o755)

                print(f"[+] Successfully compiled and installed whisper.cpp binary to {LOCAL_BIN}")
                return True

        except Exception as e:
            logger.error(f"Failed to build whisper.cpp: {e}")
            print(f"[-] whisper.cpp build error: {e}")
            return False

        return False

    @classmethod
    def install_vosk(cls) -> bool:
        """Ensure Vosk model directories are initialized."""
        model_dir = Path(HOME) / ".cache" / "termux-stt" / "models" / "vosk"
        model_dir.mkdir(parents=True, exist_ok=True)
        return True

    @classmethod
    def install_sherpa_onnx(cls) -> bool:
        """Ensure Sherpa ONNX model directories are initialized."""
        model_dir = Path(HOME) / ".cache" / "termux-stt" / "models" / "sherpa"
        model_dir.mkdir(parents=True, exist_ok=True)
        return True

    @classmethod
    def check_engine_installed(cls, engine: str) -> bool:
        """Check if an engine is installed and available in PATH."""
        if engine == "whisper":
            return bool(
                shutil.which("whisper-cli")
                or shutil.which("whisper-cpp")
                or (PREFIX_BIN / "whisper-cli").exists()
                or (PREFIX_BIN / "whisper-cpp").exists()
                or (LOCAL_BIN / "whisper-cli").exists()
                or (LOCAL_BIN / "whisper-cpp").exists()
            )
        elif engine == "vosk":
            return True
        elif engine == "sherpa":
            return bool(shutil.which("sherpa-onnx-offline") or (LOCAL_BIN / "sherpa-onnx-offline").exists())
        return False

    @classmethod
    def install_all(cls) -> Dict[str, bool]:
        """Execute 1-Click complete provisioning pipeline."""
        cls.install_system_dependencies()
        return {
            "whisper": cls.install_whisper_cpp(),
            "vosk": cls.install_vosk(),
            "sherpa": cls.install_sherpa_onnx(),
        }


def main():
    """CLI entrypoint for termux-stt-install & termux-stt install."""
    print("==========================================================")
    print("[AMEVA-Forge] termux-stt 1-Click Environment & Engine Installer")
    print("==========================================================")
    print("Setting up native dependencies and on-device STT engines for Termux...\n")

    results = EngineInstaller.install_all()
    print("\n--- Installation Summary ---")
    for engine, ok in results.items():
        status = "[OK]" if ok else "[SKIPPED/FAILED]"
        print(f" - {engine:10s} : {status}")

    print("\n[+] Setup complete. Run 'termux-stt doctor' to verify system health.")


if __name__ == "__main__":
    main()

