# Changelog

All notable changes to 	ermux-stt will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.1.6] - 2026-09-05

### Changed
- Migrated hardware acceleration dependency to unified `ameva-runtime>=2.0.0` and `@ameva/runtime>=2.0.0`.
- Pinned Whisper.cpp Vulkan backend integration with ARM Mali and Qualcomm Adreno silicon-aware routing.

---

## [1.1.4] - 2026-09-02

### Added
- **Hybrid Speech Engine**: Unified runtime across Whisper.cpp, Vosk, and Sherpa-ONNX.
- **Mobile Guard**: Memory budget validation and thermal throttling guard.

### Fixed
- **Benchmark RTF Calculation**: Removed hardcoded 10.0s fallback and added honest N/A handling when audio metadata is unreadable.
- **Engine Load Exception Propagation**: Stored and propagated import errors to callers.

### Verification
- **Unit Tests**: 43 / 43 passed with 100% assertion coverage.