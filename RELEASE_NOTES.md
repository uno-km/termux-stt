# Release Notes - termux-stt v1.3.1

**Release Tag**: `v1.3.1`  
**Distribution Channels**: PyPI (`termux-stt`), NPM (`termux-stt`), GitHub Releases  
**Target Platform**: Android Termux (ARM64 / aarch64 Bionic)  
**License**: Apache-2.0  

---

## Highlights & Key Architectural Changes

### 1. Asymmetric Mobile SoC Hybrid Pipeline (Encoder Vulkan GPU / Decoder CPU SIMD)
- **Dense GEMM & Autoregressive Decoupling**: Solves the fundamental mobile inference bottleneck where single-token sequential autoregressive decoding suffers from excessive GPU dispatch latency and pipeline stall. Offloads heavy 2D audio mel convolution & dense GEMM attention matrices entirely to Vulkan GPU compute pipelines, while keeping sequential single-token autoregressive decoding on host ARM NEON CPU SIMD vector units.
- **Cross-Attention KV Cache DMA Zero-Copy Transfer**: Automatically transfers calculated intermediate key-value projections ($K_{cross}, V_{cross}$) from Vulkan device-local storage to CPU host memory buffer (`wstate.kv_cross_cpu`) across independent GGML execution schedulers, guaranteeing 100% numerical invariance.
- **Latency & Thermal Benchmarks**:
  - **Whisper Small (60.59s JFK Audio)**: Achieves **12.93s** wall-clock time on Snapdragon 8 Elite (Galaxy S25), delivering a **21.0% speedup** over Pure GPU (16.36s) and **16.5% speedup** over Pure CPU (15.48s).
  - **Whisper Large-v3-Turbo**: Delivers **86.52s** wall-clock time (28.5s faster than Pure CPU's 115.05s) while completely freeing host CPU cores during the initial ~80s audio encoding phase, eliminating CPU thermal throttling and battery drain.
- **Upstream Open Source Contribution**: Contributed back to `ggml-org/whisper.cpp` via official [PR #4089](https://github.com/ggml-org/whisper.cpp/pull/4089).

### 2. Dynamic CLI Controls & Fail-Fast Protection
- **CLI Options**:
  - `--split-mode` / `-sm` / `--hybrid` / `--optimize-gpu-cpu`: Orchestrates Vulkan GPU encoder offloading with CPU decoder inference.
  - `--optimize-1`: Enables hybrid split mode with 1 low-power background CPU thread for decoding, providing maximum thermal headroom on asymmetric big.LITTLE clusters.
  - `--no-split-mode`: Forces monolithic pure-GPU execution if explicitly requested.
- **Fail-Fast Validation**: Instantly verifies active Vulkan device availability and raises a descriptive runtime error if `--split-mode` is requested on non-GPU environments.

### 3. Unified Universal Native Binary Distribution
- **Multi-SoC Mobile Silicon Verification**: Shipped unified binary archive `whisper-cli-android-arm64-v1.3.0.tar.gz` (SHA-256: `beab899246eb98335b519657c16515b8be4674d73a965e0e17308ab4f3115296`) verified across:
  - Qualcomm Snapdragon 8 Elite (Adreno 830) - Galaxy S25
  - Samsung Exynos 2100 (ARM Mali-G78) - Galaxy S21
  - Samsung Exynos 990 (ARM Mali-G77) - Galaxy S20
  - Samsung Exynos 1380 (ARM Mali-G68) - Galaxy A35
  - Samsung Exynos 1280 (ARM Mali-G68) - Galaxy A53
- **Bionic Zero-Collision Invariant**: Completely sanitizes Termux userland dynamic linker pollution to guarantee crash-free runtime on Android 10 through Android 15.

---

## Detailed Changelog & Asset Hashes

### Artifact Verification
| Asset Filename | Target Architecture | SHA-256 Checksum |
| :--- | :--- | :--- |
| `whisper-cli-android-arm64.tar.gz` | Android ARM64 (Bionic) | `beab899246eb98335b519657c16515b8be4674d73a965e0e17308ab4f3115296` |
| `whisper-cli-vulkan-android-arm64.tar.gz` | Android ARM64 (Bionic) | `beab899246eb98335b519657c16515b8be4674d73a965e0e17308ab4f3115296` |
| `whisper-cli-android-arm64-v1.3.0.tar.gz` | Android ARM64 (Bionic) | `beab899246eb98335b519657c16515b8be4674d73a965e0e17308ab4f3115296` |
