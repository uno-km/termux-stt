# Release Notes - termux-stt v1.3.2

**Release Tag**: `v1.3.2`  
**Distribution Channels**: PyPI (`termux-stt`), NPM (`termux-stt`), GitHub Releases  
**Target Platform**: Android Termux (ARM64 / aarch64 Bionic)  
**License**: Apache-2.0  

---

## Highlights & Key Architectural Changes

### 1. SmartRouter Dynamic Split-Mode Filtering (`whisper_engine.py`)
- **Dynamic `-sm` Option Stripping**: Automatically inspects the installed `whisper-cli` native binary capabilities. When running on binary builds that do not support split-mode flags, `-sm` is transparently filtered out to prevent execution aborts.
- **Fail-Fast Device Fallback**: Transparently transitions to pure CPU NEON mode when GPU allocation or Vulkan context initialization fails.

### 2. Thread Flag `-t` De-Duplication
- **Single Authoritative Parameter**: Resolves CLI argument collisions where both default engine configuration and SmartRouter injected duplicate `-t <threads>` arguments. Updates in-place with single authoritative thread specification.

### 3. Conditional Vulkan Backend Request
- **Constrained Backend Dispatch**: Restricts `requested_backend="vulkan"` strictly to explicit GPU/Vulkan target execution, preventing spurious driver inquiries on pure CPU targets.

### 4. Upstream Model Registry Hash Alignment (`registry.py`)
- **SHA-256 Checksums Synchronized**: Aligned SHA-256 checksums and model download URLs for Whisper quantized GGML models in the central registry.

---

## Detailed Changelog

### Fixed & Hardened
- `termux_stt/engine/whisper_engine.py`: Added split-mode capability filter, `-t` de-duplication, and conditional Vulkan backend request.
- `termux_stt/__init__.py`: Version bumped to `1.3.2`.
- `pyproject.toml` & `package.json` & `setup.py`: Version synchronized to `1.3.2`.
- `doc.config.yaml`: Documentation schema and version updated to `v1.3.2`.
