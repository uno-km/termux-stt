# Changelog

All notable changes to the `termux-stt` framework are documented in this file.

## [v1.1.3] - 2026-08-27
### Added & Polished
- **Polished CLI Error Handling**: Replaced uncaught Python tracebacks with clean, actionable error messages for file not found, model errors, and permissions.
- **Android Root `/tmp` Auto-Redirection**: Automatically detects read-only `/tmp` and routes outputs to safe writable locations (`$TMPDIR` or local directory).
- **Turn-Taking Diarization Fallback**: Auto-assigns `Speaker_0` / `Speaker_1` turns based on speech pause boundaries when acoustic models are uninitialized.

## [v1.1.2] - 2026-08-27
### Fixed & Hardened
- **100% Static Standalone Linking**: Configured `-DBUILD_SHARED_LIBS=OFF` in CMake pipeline to embed `libwhisper.a` and `libggml.a` directly into `whisper-cli`, eliminating `libwhisper.so.1 not found` runtime failures.
- **Universal Release Asset**: Uploaded self-contained ARM64 Bionic executable to GitHub Releases `v1.1.2` for zero-compilation 1-second installs across all Android devices.

## [v1.1.1] - 2026-08-27
### Added & Optimized
- **Zero-Compilation Prebuilt ARM64 Dispatch**: Integrated 1-second direct download for pre-compiled ARM64 Bionic whisper-cli binaries in `EngineInstaller`.
- **Lightweight System Dependencies**: Defers heavy `clang`, `cmake`, and `make` installation to the offline fallback stage, drastically reducing initial setup time and mobile storage usage.
- **Direct GitHub Release Manual**: Updated documentation and READMEs for pip and npm with explicit manual curl installation one-liners.

## [v1.1.0] - 2026-08-26
### Added
- **Fuzzy Typo Suggestion**: `difflib`-based model recommendations and catalog guidance upon misspelled model identifiers.
- **Output Directory Auto-Creation**: Recursive auto-creation of missing parent directories during CLI transcribe/diarize.

---

## [v1.0.8] - 2026-08-26
### Fixed & Optimized (5-Point Hardening)
- **Temp WAV Garbage Collection**: Wrapped `transcribe()` and `diarize()` with `try...finally` blocks to guarantee automatic removal of converted 16kHz WAV files, eliminating mobile storage leaks.
- **Psutil Safe Import Guard**: Isolated top-level `psutil` import in `MobileGuard` with lazy fallback to prevent `ModuleNotFoundError` on minimal environments.
- **Platform Spoofing Isolation**: Restricted `sys.platform = 'linux'` spoofing strictly to Android/Termux environments, preserving host OS isolation on Windows/macOS.
- **Mobile 1-Pass Greedy Policy**: Automatically enabled `--no-fallback` (`-nf`) on Termux to prevent multi-temperature retry loops and mobile thermal throttling.
- **Node.js Python Runtime Resolver**: Enhanced `bin/termux-stt.js` to search `python3` first before falling back to `python`.

---

## [v1.0.7] - 2026-08-26
### Fixed
- **Model Hub Variable Order**: Resolved `NameError: req` in `ModelHub.download_model` by declaring request headers prior to URL opening.
- **CLI Default Cache Priority**: Defaulted `diarize` and `benchmark` CLIs to pre-cached `tiny` model for instant 0-second execution.

---

## [v1.0.6] - 2026-08-26
### Added & Fixed
- **Flexible EngineConfig Aliasing**: Extended `EngineConfig.__init__` with backwards-compatible keyword alias mappings (`model_path`, `language`, `num_threads`, `use_vad`).
- **CLI Factory Standardization**: Migrated `diarize`, `benchmark`, and `listen` CLIs to unified `create_engine` factory.
- **Precise Header Duration**: Exact audio duration extraction from RIFF headers in benchmark CLI.
- **SSL Fallback**: Added unverified SSL context fallback for restricted network and certificate environments.

---

## [v1.0.5] - 2026-08-26
### Added & Fixed
- **Official Sample Audio**: Included clean 60.00s 16kHz Mono PCM JFK Inaugural Address sample audio (`samples/jfk_1min.wav`).
- **Zero-Subprocess Wave Parsing**: Direct pure-Python `wave` parser integration to bypass FFmpeg subprocessing for standard 16kHz WAVs.
- **Bionic Dynamic Linker Defense**: Auto-provisioning of `libbluray` and `libxml2` in `termux-stt install`.
- **1-Click Self-Contained Installer**: Integrated `termux-stt install` and `termux-stt-install` CLI entry points.
- **Dual-Engine Monorepo Packaging**: Integrated root `package.json` for seamless `npm install -g git+...` deployment.

---

## [v1.0.0] - 2026-08-20
### Added
- Initial public release of unified on-device STT & 128d X-Vector speaker diarization framework.
- Triple engine support: `whisper.cpp`, `vosk`, `sherpa-onnx`.
- Pure-Python closed-form K-Means and Cosine Distance matrix clustering.
- Subprocess crash isolation and Android mobile safeguards (WakeLock, Doze bypass).
