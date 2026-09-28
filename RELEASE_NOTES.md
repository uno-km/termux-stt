# Release Notes - termux-stt v1.2.13

**Release Tag**: `v1.2.13`  
**Distribution Channels**: PyPI (`termux-stt`), NPM (`termux-stt`), GitHub Releases  
**Target Platform**: Android Termux (ARM64 / aarch64 Bionic)  
**License**: MIT  

---

## Highlights & Key Architectural Changes

### 1. Vosk STT Runtime Dependency Auto-Provisioning
- **Self-Healing Python Bindings**: `termux_stt/platform/installer.py` now automatically detects and installs essential runtime bindings (`cffi>=1.15.0`, `srt>=3.5.0`) required for Vosk speech recognition when running on Android Termux.
- **Fail-Fast Error Mitigation**: Prevents missing CFFI/SRT import errors during cold execution on fresh Termux environments.

### 2. Zero-Drift Full SemVer Synchronization
- **Strict Package Parity**: Synchronized package manifests across `pyproject.toml`, `setup.py`, `package.json`, and `termux_stt/__init__.py` to `1.2.13`.
- **Runtime Dependencies**: Formalized explicit dependencies `cffi` and `srt` in Python package declarations.

---

## Detailed Changelog

### Fixed & Hardened
- `termux_stt/platform/installer.py`: Added automatic `cffi` and `srt` inspection and installation during Vosk provisioning.
- `pyproject.toml` & `setup.py`: Declared `cffi>=1.15.0` and `srt>=3.5.0` dependencies.
- `package.json`: Synchronized version to `1.2.13`.
- `CHANGELOG.md`: Added release summary for `v1.2.13`.
