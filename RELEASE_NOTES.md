# Release Notes - termux-stt v1.3.3

**Release Tag**: `v1.3.3`  
**Distribution Channels**: PyPI (`termux-stt`), NPM (`termux-stt`), GitHub Releases  
**Target Platform**: Android Termux (ARM64 / aarch64 Bionic)  
**License**: Apache-2.0  

---

## Highlights & Key Architectural Changes

### 1. Unified 5-Backend Standardization
- **Ecosystem Whitelist Governance**: Aligned all CLI subcommands (`transcribe`, `stream`, `diarize`) to the standard 5-backend options: `["auto", "gpu", "vulkan", "opencl", "cpu"]`.
- **Fail-Fast Defense**: Rejected unauthorized options like `cpu_neon` with strict parameter diagnostics.

### 2. Zero-Regression Full Test Pass
- **Complete Test Coverage**: Validated 57 passed tests across Whisper hybrid routing, Vosk engine, Sherpa-ONNX, and audio preprocessing without errors.
