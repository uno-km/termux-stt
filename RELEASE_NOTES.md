# Release Notes - termux-stt v1.2.12

**Release Tag**: `v1.2.12`  
**Distribution Channels**: PyPI (`termux-stt`), NPM (`termux-stt`), GitHub Releases  
**Target Platform**: Android Termux (ARM64 / aarch64 Bionic)  
**License**: MIT  

---

## Highlights & Key Architectural Changes

### 1. 100% Zero-Hardcoding Dynamic Provisioning Architecture
- **Purged Static Version Fallbacks**: Permanently eliminated all static fallback strings (`1.2.7`) from `termux_stt/platform/installer.py`.
- **Unified 3-Tier Resolution Protocol**:
  1. **Tier 1 (Explicit Environment Overrides)**: Prioritizes `TERMUX_STT_RELEASE_BASE` and `TERMUX_STT_RELEASE_TAG`.
  2. **Tier 2 (GitHub Releases Latest Canonical SSOT)**: Directly fetches canonical unversioned binaries (`whisper-cli-android-arm64.tar.gz`, `sherpa-onnx-android-arm64.tar.gz`, `vosk-android-arm64.tar.gz`) from `https://github.com/uno-km/termux-stt/releases/latest/download/`.
  3. **Tier 3 (Runtime Dynamic Version Resolution)**: Leverages dynamic package introspection without hardcoded fallback strings.
- **Dynamic HTTP User-Agent**: Replaced static user-agent headers with dynamic package version introspection (`termux-stt-installer/{ver}`).

### 2. Default Whisper Tiny Model Invariant Mirror
- **Latest Canonical Model Endpoint**: Updated default `tiny` model registry entry to pull directly from `https://github.com/uno-km/termux-stt/releases/latest/download/ggml-tiny.bin` with SHA-256 integrity verification (`be07e048...`).

### 3. Unified Pip & NPM Packaging Parity
- **Full SemVer Synchronization**: Synchronized `pyproject.toml`, `setup.py`, `termux_stt/__init__.py`, and `package.json` to `1.2.12`.
- **Transparent Node Runner**: `npx termux-stt` routes commands directly to the local Bionic Python/C++ runtime with zero latency.

---

## Detailed Changelog

### Changed
- `termux_stt/platform/installer.py`: Replaced static release URLs with prioritized 3-Tier candidate URL generator.
- `termux_stt/models/registry.py`: Pointed `tiny` model to latest invariant release endpoint.
- `CHANGELOG.md`: Added release summary for `v1.2.12`.
- Package manifests (`pyproject.toml`, `package.json`, `setup.py`, `termux_stt/__init__.py`) bumped to `1.2.12`.

### Removed
- Legacy static URL candidates pointing to deprecated staging releases.
