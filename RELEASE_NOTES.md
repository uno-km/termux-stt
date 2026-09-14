# Termux-STT Release Notes

## [1.2.5] - 2026-09-14

### Major Highlights
- **Qualcomm Adreno Vulkan Native Acceleration & SoftMax wg64 Alignment**:
  - Resolved physical device lost (VK_ERROR_DEVICE_LOST) and cross-warp barrier deadlock on Qualcomm Adreno GPUs (Snapdragon 8 Gen 1 / Adreno 730) by strictly constraining Vulkan SoftMax workgroups to hardware subgroup size (64).
  - Implemented automatic hardware-aware routing in Whisper core: automatically bypasses closed-source Qualcomm driver compiler crashes on Flash Attention, routing directly to the 100% native Vulkan GPU standard attention pipeline without requiring manual --no-flash-attn (-nfa) CLI flags.
  - **Empirical Ground-Truth Speedup**: Galaxy S22 (Adreno 730) achieves **3.73x speedup in neural encoder time (19.14s CPU -> 5.13s GPU)** with zero silent fallback (fallbacks = 0 p / 0 h) and ~14% CPU load.
- **ARM Mali-G78 Flash Attention GPU Non-Regression**:
  - Non-Qualcomm GPUs (e.g. ARM Mali-G78 on Galaxy S21) continue to utilize native Vulkan Flash Attention (~17.5s total inference time, zero fallbacks).
- **Zero-Silent-Fallback & Single Bundle SSOT**:
  - Native asset installer provisions verified whisper-cli-vulkan-android-arm64.tar.gz with full Bionic RPATH bindings (/../lib:).
  - Added -ng flag support when CPU execution is explicitly requested (-d cpu).
