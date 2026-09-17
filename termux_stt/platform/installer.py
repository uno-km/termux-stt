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
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

PREFIX = os.environ.get("PREFIX", "/data/data/com.termux/files/usr")
HOME = os.environ.get("HOME", os.path.expanduser("~"))
XDG_CACHE_HOME = Path(os.environ.get("XDG_CACHE_HOME") or (Path(HOME) / ".cache"))
PREFIX_BIN = Path(PREFIX) / "bin"
PREFIX_LIB = Path(PREFIX) / "lib"


class EngineInstaller:
    """Automated installer for native dependencies and C++ engines."""

    @classmethod
    def get_candidate_whisper_urls(cls) -> List[str]:
        """Generate dynamic SSOT candidate URLs for standard pure-CPU engine."""
        try:
            from .. import __version__
        except Exception:
            __version__ = "1.2.7"

        urls = []
        custom_tag = os.environ.get("TERMUX_STT_RELEASE_TAG", "").strip()
        custom_base = os.environ.get("TERMUX_STT_RELEASE_BASE", "").strip()

        if custom_base:
            base = custom_base.rstrip("/")
            urls.append(f"{base}/whisper-cli-android-arm64.tar.gz")
        if custom_tag:
            tag = custom_tag if custom_tag.startswith("v") else f"v{custom_tag}"
            urls.append(f"https://github.com/uno-km/termux-stt/releases/download/{tag}/whisper-cli-android-arm64.tar.gz")

        # Current version SSOT (Pure CPU No-Build)
        current_tag = f"v{__version__}"
        urls.append(f"https://github.com/uno-km/termux-stt/releases/download/{current_tag}/whisper-cli-android-arm64.tar.gz")

        # Latest release on termux-stt
        urls.append("https://github.com/uno-km/termux-stt/releases/latest/download/whisper-cli-android-arm64.tar.gz")

        return urls

    @classmethod
    def get_candidate_sherpa_urls(cls) -> List[str]:
        """Generate dynamic SSOT candidate URLs for prebuilt sherpa-onnx + onnxruntime engine."""
        try:
            from .. import __version__
        except Exception:
            __version__ = "1.2.7"

        urls = []
        custom_tag = os.environ.get("TERMUX_STT_RELEASE_TAG", "").strip()
        custom_base = os.environ.get("TERMUX_STT_RELEASE_BASE", "").strip()

        if custom_base:
            base = custom_base.rstrip("/")
            urls.append(f"{base}/sherpa-onnx-android-arm64.tar.gz")
        if custom_tag:
            tag = custom_tag if custom_tag.startswith("v") else f"v{custom_tag}"
            urls.append(f"https://github.com/uno-km/termux-stt/releases/download/{tag}/sherpa-onnx-android-arm64.tar.gz")

        # Current version SSOT
        current_tag = f"v{__version__}"
        urls.append(f"https://github.com/uno-km/termux-stt/releases/download/{current_tag}/sherpa-onnx-android-arm64.tar.gz")

        # Latest release on termux-stt
        urls.append("https://github.com/uno-km/termux-stt/releases/latest/download/sherpa-onnx-android-arm64.tar.gz")

        return urls

    @classmethod
    def get_candidate_vosk_urls(cls) -> List[str]:
        """Generate dynamic SSOT candidate URLs for prebuilt vosk-android engine."""
        try:
            from .. import __version__
        except Exception:
            __version__ = "1.2.7"

        urls = []
        custom_tag = os.environ.get("TERMUX_STT_RELEASE_TAG", "").strip()
        custom_base = os.environ.get("TERMUX_STT_RELEASE_BASE", "").strip()

        if custom_base:
            base = custom_base.rstrip("/")
            urls.append(f"{base}/vosk-android-arm64.tar.gz")
        if custom_tag:
            tag = custom_tag if custom_tag.startswith("v") else f"v{custom_tag}"
            urls.append(f"https://github.com/uno-km/termux-stt/releases/download/{tag}/vosk-android-arm64.tar.gz")

        # Current version SSOT
        current_tag = f"v{__version__}"
        urls.append(f"https://github.com/uno-km/termux-stt/releases/download/{current_tag}/vosk-android-arm64.tar.gz")

        # Latest release on termux-stt
        urls.append("https://github.com/uno-km/termux-stt/releases/latest/download/vosk-android-arm64.tar.gz")

        return urls

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
    def _print_remediation_guide(cls):
        """Print clear, structured remediation guide for updating termux-stt."""
        print("\n" + "=" * 76)
        print("[AMEVA-STT-E001] Native whisper.cpp binary acquisition failed.")
        print("=" * 76)
        print("To install or upgrade the standard engine:")
        print("  - Python / Pip: pip install -U termux-stt && termux-stt install")
        print("  - Node.js / NPM: npm install -g termux-stt@latest")
        print("For 10x Native Vulkan GPU Turbo Acceleration:")
        print("  - Install AMEVA Runtime: pip install ameva-runtime")
        print("============================================================================" + "\n")

    @classmethod
    def _download_prebuilt_whisper(cls) -> bool:
        """Attempt to download and stream-extract precompiled ARM64 Bionic whisper-cli binary (~3s)."""
        import io
        import tarfile
        import urllib.request
        try:
            from .. import __version__
        except Exception:
            __version__ = "1.2.7"

        PREFIX_BIN.mkdir(parents=True, exist_ok=True)
        PREFIX_LIB.mkdir(parents=True, exist_ok=True)
        staging_dir = XDG_CACHE_HOME / "termux-stt" / ".staging-whisper"
        staging_dir.mkdir(parents=True, exist_ok=True)
        target_path = PREFIX_BIN / "whisper-cli"

        print("[*] Attempting Fast-Track direct download of pre-compiled whisper.cpp ARM64 Vulkan binary...")
        candidate_urls = cls.get_candidate_whisper_urls()
        for url in candidate_urls:
            try:
                req = urllib.request.Request(
                    url,
                    headers={"User-Agent": f"termux-stt-installer/{__version__} (Android; ARM64)"}
                )
                with urllib.request.urlopen(req, timeout=15) as response:
                    content = response.read()

                if not content or len(content) < 100 * 1024:
                    continue

                # Check if gzip tarball (magic 0x1F, 0x8B)
                is_tar = content[:2] == b'\x1f\x8b' or url.endswith(".tar.gz")
                if is_tar:
                    with tarfile.open(fileobj=io.BytesIO(content), mode="r:gz") as tar:
                        tar.extractall(path=staging_dir)

                    # Locate whisper-cli or main in staging
                    found_bin = None
                    for p in staging_dir.rglob("*"):
                        if p.is_file() and p.name in ("whisper-cli", "whisper-cpp", "main"):
                            found_bin = p
                            break

                    if found_bin:
                        shutil.copy2(found_bin, target_path)
                        target_path.chmod(0o755)
                        shutil.copy2(target_path, PREFIX_BIN / "whisper-cpp")
                        (PREFIX_BIN / "whisper-cpp").chmod(0o755)

                    # Extract any shared libraries to PREFIX_LIB
                    for so_file in staging_dir.rglob("*.so*"):
                        if so_file.is_file():
                            target_so = PREFIX_LIB / so_file.name
                            shutil.copy2(so_file, target_so)
                            try:
                                target_so.chmod(0o755)
                            except OSError:
                                pass

                    shutil.rmtree(staging_dir, ignore_errors=True)
                else:
                    with open(target_path, "wb") as out_file:
                        out_file.write(content)
                    target_path.chmod(0o755)
                    shutil.copy2(target_path, PREFIX_BIN / "whisper-cpp")
                    (PREFIX_BIN / "whisper-cpp").chmod(0o755)

                # Check if downloaded file is valid executable (>100KB)
                if target_path.exists() and target_path.stat().st_size > 100 * 1024:
                    print(f"[+] Pre-compiled whisper.cpp binary successfully installed to {target_path} (from {url})")
                    return True
                else:
                    if target_path.exists():
                        target_path.unlink()
            except Exception as e:
                logger.debug(f"Prebuilt download attempt failed for {url}: {e}")
                shutil.rmtree(staging_dir, ignore_errors=True)
                continue

        print("[-] Pre-built Vulkan binary download unavailable from candidate mirrors.")
        cls._print_remediation_guide()
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
        """Install whisper.cpp: Priority 1 = Pre-built download (~3s), Priority 2 = Local build (cmake/clang)."""
        PREFIX_BIN.mkdir(parents=True, exist_ok=True)
        PREFIX_LIB.mkdir(parents=True, exist_ok=True)

        # Check bundled package binary first
        bundled_bin = Path(__file__).resolve().parent.parent / "bin" / "whisper-cli"
        if bundled_bin.exists() and bundled_bin.stat().st_size > 100 * 1024:
            try:
                shutil.copy2(bundled_bin, PREFIX_BIN / "whisper-cli")
                (PREFIX_BIN / "whisper-cli").chmod(0o755)
                shutil.copy2(bundled_bin, PREFIX_BIN / "whisper-cpp")
                (PREFIX_BIN / "whisper-cpp").chmod(0o755)
                print(f"[+] Deployed bundled whisper.cpp binary from package to {PREFIX_BIN}")
                return True
            except OSError as _b_err:
                logger.debug("Failed copying bundled binary: %s", _b_err)

        # Check existing binary
        for candidate in [PREFIX_BIN / "whisper-cli", PREFIX_BIN / "whisper-cpp"]:
            if candidate.exists() and os.access(str(candidate), os.X_OK):
                print(f"[+] whisper.cpp binary is already present at {candidate}.")
                return True

        # Priority 1: Fast Direct Pre-built Stream Download (~3s, Vulkan+NEON enabled)
        if cls._download_prebuilt_whisper():
            return True

        # Priority 2: Fallback to Local CMake & Clang compilation
        print("[*] Setting up whisper.cpp native engine via local compiler with ARM NEON...")
        if shutil.which("pkg"):
            subprocess.run(["pkg", "install", "-y", "cmake", "make", "clang"], check=False)

        build_dir = XDG_CACHE_HOME / "termux-stt" / "build" / "whisper.cpp"
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
                for target_name in ["whisper-cli", "whisper-cpp"]:
                    shutil.copy2(bin_source, PREFIX_BIN / target_name)
                    (PREFIX_BIN / target_name).chmod(0o755)

                # Copy any built .so to PREFIX_LIB
                for so_file in (build_dir / "build").rglob("*.so*"):
                    if so_file.is_file():
                        target_so = PREFIX_LIB / so_file.name
                        shutil.copy2(so_file, target_so)
                        try:
                            target_so.chmod(0o755)
                        except OSError:
                            pass

                print(f"[+] Successfully compiled and installed whisper.cpp binary to {PREFIX_BIN}")
                return True

        except Exception as e:
            logger.error(f"Failed to build whisper.cpp: {e}")
            print(f"[-] whisper.cpp build error: {e}")
            cls._print_remediation_guide()
            return False

        cls._print_remediation_guide()
        return False

    @classmethod
    def _download_prebuilt_sherpa(cls) -> bool:
        """Download and stream-extract precompiled sherpa-onnx & onnxruntime binaries (~3s)."""
        import io
        import tarfile
        import urllib.request
        try:
            from .. import __version__
        except Exception:
            __version__ = "1.2.7"

        PREFIX_BIN.mkdir(parents=True, exist_ok=True)
        PREFIX_LIB.mkdir(parents=True, exist_ok=True)
        staging_dir = XDG_CACHE_HOME / "termux-stt" / ".staging-sherpa"
        staging_dir.mkdir(parents=True, exist_ok=True)

        print("[*] Downloading pre-compiled sherpa-onnx & ONNX Runtime ARM64 engine (~23MB)...")
        candidate_urls = cls.get_candidate_sherpa_urls()
        for url in candidate_urls:
            try:
                req = urllib.request.Request(
                    url,
                    headers={"User-Agent": f"termux-stt-installer/{__version__} (Android; ARM64)"}
                )
                with urllib.request.urlopen(req, timeout=30) as response:
                    content = response.read()

                if not content or len(content) < 100 * 1024:
                    continue

                is_tar = content[:2] == b'\x1f\x8b' or url.endswith(".tar.gz")
                if is_tar:
                    with tarfile.open(fileobj=io.BytesIO(content), mode="r:gz") as tar:
                        tar.extractall(path=staging_dir)

                    # Deploy binaries to PREFIX_BIN
                    for p in staging_dir.rglob("sherpa-onnx*"):
                        if p.is_file():
                            target = PREFIX_BIN / p.name
                            shutil.copy2(p, target)
                            try:
                                target.chmod(0o755)
                            except OSError:
                                pass

                    # Deploy shared libraries (onnxruntime, sherpa-c-api) to PREFIX_LIB
                    for so_file in staging_dir.rglob("*.so*"):
                        if so_file.is_file():
                            target_so = PREFIX_LIB / so_file.name
                            shutil.copy2(so_file, target_so)
                            try:
                                target_so.chmod(0o755)
                            except OSError:
                                pass

                    shutil.rmtree(staging_dir, ignore_errors=True)

                    if (PREFIX_BIN / "sherpa-onnx-offline").exists():
                        print(f"[+] Successfully installed pre-compiled sherpa-onnx & onnxruntime to {PREFIX_BIN} and {PREFIX_LIB}")
                        return True
            except Exception as e:
                logger.debug(f"Sherpa download attempt failed for {url}: {e}")
                shutil.rmtree(staging_dir, ignore_errors=True)
                continue

        print("[-] Pre-built sherpa-onnx binary download unavailable from candidate mirrors.")
        return False

    @classmethod
    def _download_prebuilt_vosk(cls) -> bool:
        """Download and extract precompiled vosk package & libvosk.so (~6.5MB)."""
        import io
        import site
        import tarfile
        import urllib.request
        try:
            from .. import __version__
        except Exception:
            __version__ = "1.2.7"

        PREFIX_LIB.mkdir(parents=True, exist_ok=True)
        # Ensure pure-python dependency 'srt' is present
        try:
            import srt  # noqa: F401
        except ImportError:
            subprocess.run(["pip", "install", "--no-cache-dir", "srt"], check=False)

        # Locate target site-packages directory
        target_site = None
        for p in site.getsitepackages():
            if "com.termux" in p and "site-packages" in p:
                target_site = Path(p)
                break
        if not target_site:
            target_site = Path(sys.prefix) / "lib" / f"python{sys.version_info.major}.{sys.version_info.minor}" / "site-packages"

        target_site.mkdir(parents=True, exist_ok=True)
        staging_dir = XDG_CACHE_HOME / "termux-stt" / ".staging-vosk"
        staging_dir.mkdir(parents=True, exist_ok=True)

        print("[*] Downloading pre-compiled vosk Bionic ARM64 engine (~6.5MB)...")
        candidate_urls = cls.get_candidate_vosk_urls()
        for url in candidate_urls:
            try:
                req = urllib.request.Request(
                    url,
                    headers={"User-Agent": f"termux-stt-installer/{__version__} (Android; ARM64)"}
                )
                with urllib.request.urlopen(req, timeout=30) as response:
                    content = response.read()

                if not content or len(content) < 100 * 1024:
                    continue

                is_tar = content[:2] == b'\x1f\x8b' or url.endswith(".tar.gz")
                if is_tar:
                    with tarfile.open(fileobj=io.BytesIO(content), mode="r:gz") as tar:
                        tar.extractall(path=staging_dir)

                    # Deploy vosk python module to site-packages
                    if (staging_dir / "vosk").exists():
                        dest_vosk = target_site / "vosk"
                        if dest_vosk.exists():
                            shutil.rmtree(dest_vosk, ignore_errors=True)
                        shutil.copytree(staging_dir / "vosk", dest_vosk)

                    # Deploy libvosk.so to PREFIX_LIB
                    for so_file in staging_dir.rglob("*.so*"):
                        if so_file.is_file():
                            target_so = PREFIX_LIB / so_file.name
                            shutil.copy2(so_file, target_so)
                            try:
                                target_so.chmod(0o755)
                            except OSError:
                                pass

                    shutil.rmtree(staging_dir, ignore_errors=True)

                    try:
                        import vosk  # noqa: F401
                        print(f"[+] Successfully installed pre-compiled vosk engine to {target_site / 'vosk'}")
                        return True
                    except Exception as _v_err:
                        logger.debug("Vosk import check after install failed: %s", _v_err)
            except Exception as e:
                logger.debug(f"Vosk download attempt failed for {url}: {e}")
                shutil.rmtree(staging_dir, ignore_errors=True)
                continue

        print("[-] Pre-built vosk binary download unavailable from candidate mirrors.")
        return False

    @classmethod
    def install_vosk(cls, auto_yes: bool = False, interactive: bool = True) -> bool:
        """Install prebuilt vosk engine and initialize cache directories."""
        model_dir = XDG_CACHE_HOME / "termux-stt" / "models" / "vosk"
        model_dir.mkdir(parents=True, exist_ok=True)
        try:
            import vosk  # noqa: F401
            print("[+] vosk is already installed.")
            return True
        except ImportError:
            pass

        if not auto_yes and interactive and sys.stdin.isatty():
            try:
                ans = input("[?] Install additional engine 'vosk' (Prebuilt Kaldi Bionic + CFFI, ~6.5MB)? [y/N]: ").strip().lower()
                if ans not in ("y", "yes"):
                    print("[*] Skipping optional vosk installation.")
                    return True
            except (EOFError, KeyboardInterrupt):
                print("\n[*] Skipping optional vosk installation.")
                return True

        # Prebuilt binary stream extraction from GitHub releases
        return cls._download_prebuilt_vosk()

    @classmethod
    def install_sherpa_onnx(cls, auto_yes: bool = False, interactive: bool = True) -> bool:
        """Install prebuilt sherpa-onnx binaries and initialize cache directories."""
        model_dir = XDG_CACHE_HOME / "termux-stt" / "models" / "sherpa"
        model_dir.mkdir(parents=True, exist_ok=True)
        if shutil.which("sherpa-onnx-offline") or (PREFIX_BIN / "sherpa-onnx-offline").exists():
            print("[+] sherpa-onnx binary is already present.")
            return True

        if not auto_yes and interactive and sys.stdin.isatty():
            try:
                ans = input("[?] Install additional engine 'sherpa-onnx' (Prebuilt ONNX Runtime + ASR/TTS/VAD, ~23MB)? [y/N]: ").strip().lower()
                if ans not in ("y", "yes"):
                    print("[*] Skipping optional sherpa-onnx installation.")
                    return True
            except (EOFError, KeyboardInterrupt):
                print("\n[*] Skipping optional sherpa-onnx installation.")
                return True

        # Prebuilt binary stream extraction (No mobile source compilation)
        return cls._download_prebuilt_sherpa()

    @classmethod
    def check_engine_installed(cls, engine: str) -> bool:
        """Check if an engine is installed and available in PATH."""
        if engine == "whisper":
            return bool(
                shutil.which("whisper-cli")
                or shutil.which("whisper-cpp")
                or (PREFIX_BIN / "whisper-cli").exists()
                or (PREFIX_BIN / "whisper-cpp").exists()
            )
        elif engine == "vosk":
            try:
                import vosk  # noqa: F401
                return True
            except ImportError:
                return False
        elif engine == "sherpa":
            return bool(shutil.which("sherpa-onnx-offline") or (PREFIX_BIN / "sherpa-onnx-offline").exists())
        return False

    @classmethod
    def install_all(
        cls,
        auto_yes: bool = False,
        interactive: bool = True,
        target_engine: Optional[str] = None
    ) -> Dict[str, bool]:
        """Execute 1-Click complete provisioning pipeline with interactive prompt support."""
        cls.install_system_dependencies()

        results = {}
        if target_engine:
            eng = target_engine.lower()
            if eng == "whisper":
                results["whisper"] = cls.install_whisper_cpp()
            elif eng == "sherpa":
                results["sherpa"] = cls.install_sherpa_onnx(auto_yes=True, interactive=False)
            elif eng == "vosk":
                results["vosk"] = cls.install_vosk(auto_yes=True, interactive=False)
            else:
                print(f"[-] Unknown engine target: {target_engine}")
                results[eng] = False
            return results

        # Standard installation: Primary engine (whisper) is mandatory
        results["whisper"] = cls.install_whisper_cpp()

        # Additional engines are prompted or skipped
        results["sherpa"] = cls.install_sherpa_onnx(auto_yes=auto_yes, interactive=interactive)
        results["vosk"] = cls.install_vosk(auto_yes=auto_yes, interactive=interactive)

        return results


def main(args=None):
    """CLI entrypoint for termux-stt-install & termux-stt install."""
    print("==========================================================")
    print("[AMEVA-Forge] termux-stt 1-Click Environment & Engine Installer")
    print("==========================================================")
    print("Setting up native dependencies and on-device STT engines for Termux...\n")

    auto_yes = getattr(args, "yes", False) or getattr(args, "all", False)
    target_engine = getattr(args, "engine", None)

    results = EngineInstaller.install_all(
        auto_yes=auto_yes,
        interactive=not auto_yes,
        target_engine=target_engine
    )
    print("\n--- Installation Summary ---")
    for engine, ok in results.items():
        status = "[OK]" if ok else "[SKIPPED/FAILED]"
        print(f" - {engine:10s} : {status}")

    # Primary engine failure causes non-zero exit in standard mode
    if target_engine and not results.get(target_engine, False):
        print(f"\n[!] Setup incomplete: failed engine: {target_engine}")
        raise SystemExit(1)
    elif not target_engine and not results.get("whisper", False):
        print("\n[!] Setup incomplete: primary engine 'whisper' failed.")
        raise SystemExit(1)

    print("\n[+] Setup complete. Run 'termux-stt doctor' to verify system health.")


if __name__ == "__main__":
    main()

