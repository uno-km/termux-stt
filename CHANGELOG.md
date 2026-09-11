# Changelog

All notable changes to 	ermux-stt will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.2.4] - 2026-09-07

### Added
- **Fast-Track Prebuilt Stream Extractor (~3s)**: Automated stream downloading and in-memory extraction of `whisper-cli-android-arm64.tar.gz` directly from GitHub Releases, avoiding 20-minute on-device C++ compilation.
- **Zero-Hardcoding SSOT Dynamic Candidates**: Replaced legacy static release URLs with dynamic candidate resolution (`TERMUX_STT_RELEASE_TAG`, `v{__version__}`, `releases/latest/download`, and `uno-km/ameva-runtime` SSOT fallback).
- **Vulkan Logic Normalization**: Fixed priority routing to treat precompiled Vulkan+NEON binaries as Priority 1 across all devices, with local CMake/Clang builds reserved strictly as offline fallbacks.
- **Bundled Package Binary Fallback**: Auto-detects and provisions bundled `termux_stt/bin/whisper-cli` if present.

---

## [1.2.3] - 2026-09-07

### Added
- Expanded Section 1 installation documentation with in-depth bundled ARM64 binary architecture details.
- Detailed 3-stage post-installation provisioner (`termux-stt install`) pipeline explanation (native system codecs, adaptive Vulkan GPU clang compilation, sub-engine ecosystem).
- Comprehensive Pure Install vs. Post-Install comparison matrix covering binary states, audio codec support, and execution speed.

---

## [1.2.2] - 2026-09-07

### Added
- Complete 12-tier enterprise English documentation overhaul for PyPI and GitHub/NPM.
- Detailed empirical mobile hardware benchmarks (Snapdragon 8 Elite / Adreno 830, Snapdragon 865, Exynos 1380 / Mali-G68 MP5).
- Full GPU interconnect architecture documentation with SPIR-V compute shader details.
- Comprehensive CPU vs. GPU thermal dissipation, latency, and power efficiency analysis.
- 3-stage 24/7 unattended background execution guide (Termux wake-lock, battery optimization, ADB phantom process killer).
- Expanded technical SEO metadata keywords (50 keywords connecting to AMEVA ecosystem).
- Packaged standalone ARM64 whisper-cli binary asset for GitHub Releases.
- Archived comprehensive engineering guides and legacy reports to ameva-foundation.

### Fixed
- Sanitized author email metadata to official foundation address.
- Removed redundant legacy `npm/` directory in favor of root single source of truth.

---

## [1.2.1] - 2026-09-07

### Fixed
- Fixed npm package.json bin path specification (removed './' prefix).
- Integrated GitHub Actions automated CI/CD release workflow.

---

## [1.2.0] - 2026-09-07

### Added
- Direct integration with `SttAdapter.get_execution_environment()` from `ameva_runtime.adapters` SSOT.
- Eliminated raw `LD_LIBRARY_PATH` pollution and enforced strict Fail-Fast on explicit Vulkan requests.
- Full English localization of diagnostic logs and error reporting.

---

## [1.1.7] - 2026-09-05

### Changed
- Resolved Node.js whisper module require bindings to `@ameva/runtime` preventing MODULE_NOT_FOUND.
- Modernized Whisper.cpp installation toolchain and hardware adapter docstrings.

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
