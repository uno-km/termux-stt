# Release Notes - termux-stt v1.2.15

**Release Tag**: `v1.2.15`  
**Distribution Channels**: PyPI (`termux-stt`), NPM (`termux-stt`), GitHub Releases  
**Target Platform**: Android Termux (ARM64 / aarch64 Bionic)  
**License**: Apache-2.0  

---

## Highlights & Key Architectural Changes

### 1. Bionic Linker Zero-Collision Rule & Android 15 Safety Gate
- **Purged LD_LIBRARY_PATH Pollution**: Resolved dynamic linker collision (`cannot locate symbol "Xzs_Construct" referenced by "/system/lib64/libunwindstack.so"`) on Android 15 (Galaxy S25) by strictly sanitizing Termux `$PREFIX/lib` out of runtime `LD_LIBRARY_PATH`.
- **Authoritative Subprocess Isolation**: Ensured that the bundled `whisper-cli` binary resolves shared objects strictly via its own `$ORIGIN:$ORIGIN/../lib` RPATH without interference from conflicting Termux userland packages.

### 2. Dual-Flagship Native Vulkan GPU Universal Acceleration (Galaxy S25 & S21 Verified)
- **Qualcomm Adreno 830 (Snapdragon 8 Elite)**: Fully unlocked native Vulkan GPU offload (`-dev 0`, SoftMax wg64) without pipeline creation failure or IEEE 754 FTZ drift. Achieved 10.28s transcription on 60s JFK audio (RTF 0.171).
- **ARM Mali-G78 (Exynos 2100)**: Enforced BDA (Buffer Device Address) deactivation and FP32 medium matmul fallback, eliminating NULL-pointer SIGSEGV crashes across mobile Mali GPUs.
- **Single Universal Binary**: Shipped unified binary bundle (`whisper-cli-android-arm64.tar.gz`, 15.28 MB) supporting both Qualcomm and Samsung flagship silicon.

---

## Detailed Changelog

### Fixed & Hardened
- `termux_stt/engine/whisper_engine.py`: Integrated `_supports_gpu` and `run_env` dynamic LD_LIBRARY_PATH sanitization.
- `termux_stt/platform/installer.py`: Updated asset hash and manifest tracking for unified Vulkan binary distribution.
- `doc.config.yaml`: Synchronized documentation specification to `v1.2.14`.
