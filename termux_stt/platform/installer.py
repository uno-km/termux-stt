"""
1-Click Self-Contained Native Engine & Dependency Installer for Termux.
Provisions ffmpeg, clang, cmake, and builds whisper.cpp with ARM NEON.
"""

import logging
import os
import shutil
import subprocess
from pathlib import Path
from typing import Dict, List

logger = logging.getLogger(__name__)

PREFIX = os.environ.get("PREFIX", "/data/data/com.termux/files/usr")
HOME = os.environ.get("HOME", os.path.expanduser("~"))
LOCAL_BIN = Path(HOME) / ".local" / "bin"
PREFIX_BIN = Path(PREFIX) / "bin"


class EngineInstaller:
    """Automated installer for native dependencies and C++ engines."""

    PREBUILT_WHISPER_URLS = [
        "https://github.com/uno-km/termux-stt/releases/download/v1.1.3/whisper-cli-arm64-android",
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
                    except OSError as _copy_err:
                        logger.debug("Copying to PREFIX_BIN failed (%s), using LOCAL_BIN only", _copy_err)

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
    def _build_cmake_flags(cls) -> List[str]:
        flags = [
            "-B", "build",
            "-DBUILD_SHARED_LIBS=OFF",
            "-DWHISPER_BUILD_SHARED=OFF",
            "-DWHISPER_NEON=ON",
            "-DCMAKE_BUILD_TYPE=Release",
        ]
        can_vulkan = False
        try:
            from ameva_runtime.vulkan.doctor import Doctor
            can_vulkan = Doctor().quick_probe()
        except ImportError:
            can_vulkan = bool(shutil.which("vulkaninfo") or os.path.exists("/system/lib64/libvulkan.so"))

        if can_vulkan:
            print("[+] Vulkan Compute GPU acceleration detected: enabling -DGGML_VULKAN=ON")
            flags.append("-DGGML_VULKAN=ON")
            if os.path.exists("/system/lib64/libvulkan.so"):
                flags.append("-DVulkan_LIBRARY=/system/lib64/libvulkan.so")
            prefix_include = Path(PREFIX) / "include"
            if (prefix_include / "vulkan").exists():
                flags.append(f"-DVulkan_INCLUDE_DIR={prefix_include}")
        else:
            print("[-] Vulkan unavailable. Building CPU-NEON optimized static binary.")
        return flags

    @classmethod
    def install_whisper_cpp(cls) -> bool:
        """Install whisper.cpp: Priority 1 = Pre-built download (CPU), Priority 2 = Local build (Vulkan/NEON)."""
        LOCAL_BIN.mkdir(parents=True, exist_ok=True)

        can_vulkan = False
        try:
            from ameva_runtime.vulkan.doctor import Doctor
            can_vulkan = Doctor().quick_probe()
        except ImportError:
            can_vulkan = bool(shutil.which("vulkaninfo") or os.path.exists("/system/lib64/libvulkan.so"))

        # Check existing binary
        for candidate in [LOCAL_BIN / "whisper-cli", PREFIX_BIN / "whisper-cli", LOCAL_BIN / "whisper-cpp", PREFIX_BIN / "whisper-cpp"]:
            if candidate.exists() and os.access(str(candidate), os.X_OK):
                from ..engine.whisper_engine import WhisperEngine
                if not can_vulkan or WhisperEngine._supports_ngl(str(candidate)):
                    print(f"[+] whisper.cpp binary is already present at {candidate}.")
                    return True
                else:
                    print(f"[*] Existing whisper.cpp binary at {candidate} is CPU-only. Rebuilding with Vulkan...")
                    break

        # Priority 1: Fast Direct Pre-built Download (only if Vulkan not available)
        if not can_vulkan:
            if cls._download_prebuilt_whisper():
                return True

        # Priority 2: Fallback to Local CMake & Clang compilation
        print("[*] Setting up whisper.cpp native engine via local compiler with ARM NEON...")
        if shutil.which("pkg"):
            subprocess.run(["pkg", "install", "-y", "cmake", "make", "clang"], check=False)

        build_dir = Path(HOME) / ".cache" / "termux-stt" / "build" / "whisper.cpp"
        build_dir.parent.mkdir(parents=True, exist_ok=True)

        try:
            if not build_dir.exists():
                print("[*] Cloning whisper.cpp repository...")
                subprocess.run(
                    ["git", "clone", "--depth", "1", "https://github.com/ggerganov/whisper.cpp.git", str(build_dir)],
                    check=True,
                )

            cmake_flags = ["cmake"] + cls._build_cmake_flags()
            print(f"[*] Configuring whisper.cpp with {' '.join(cmake_flags)}...")
            subprocess.run(
                cmake_flags,
                cwd=str(build_dir),
                check=True,
            )
            nproc = os.cpu_count() or 4
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
                    except OSError as _copy_err:
                        logger.debug("Copying compiled binary to PREFIX_BIN failed (%s), using LOCAL_BIN only", _copy_err)
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
        """Install vosk Python package and initialize cache directories."""
        model_dir = Path(HOME) / ".cache" / "termux-stt" / "models" / "vosk"
        model_dir.mkdir(parents=True, exist_ok=True)
        try:
            import vosk  # noqa: F401
            return True
        except ImportError:
            print("[*] Installing vosk Python binding via pip...")
            res = subprocess.run(["pip", "install", "vosk"], check=False)
            return res.returncode == 0

    @classmethod
    def install_sherpa_onnx(cls) -> bool:
        """Install sherpa-onnx and initialize cache directories."""
        model_dir = Path(HOME) / ".cache" / "termux-stt" / "models" / "sherpa"
        model_dir.mkdir(parents=True, exist_ok=True)
        if shutil.which("sherpa-onnx-offline") or (LOCAL_BIN / "sherpa-onnx-offline").exists():
            return True
        print("[*] Installing sherpa-onnx via pip...")
        res = subprocess.run(["pip", "install", "sherpa-onnx"], check=False)
        return res.returncode == 0

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
            try:
                import vosk  # noqa: F401
                return True
            except ImportError:
                return False
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

