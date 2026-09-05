# Termux-STT Release Notes

## Termux-STT v1.1.8 Release Notes

**Release Date:** September 5, 2026  
**Artifact ID:** `termux-stt-1.1.8`  
**Compliance Standard:** OpenSSF Best Practices, CNCF Zero-Emoji Standard  

---

### Key Highlights
- **Zero-Configuration On-Demand Demo Pipeline**: Introduced `termux-stt demo` and `termux-stt transcribe --demo`. The CLI automatically resolves and caches the 1-minute JFK benchmark speech audio (`~/.cache/termux-stt/samples/jfk_1min.wav`) with fail-fast HTTP integrity checks.
- **NPM Package Optimization & Debloating**: Removed redundant duplicate 1.92 MB WAV audio payloads from the NPM distribution bundle. Decreased npm package footprint significantly while maintaining complete developer test fidelity via repository samples.
- **Ecosystem Runtime Alignment**: Synchronized core dependencies with `ameva-runtime>=2.1.0`.
- **Packaging Cleanliness**: Untracked legacy archive artifacts and added strict `.tgz` exclusion rules.

---

## Termux-STT v1.1.3 Release Notes

## 🚀 Key Highlights
- **Friendly Top-Level CLI Exception Handling**: Replaced raw, aggressive Python stack traces with polished, informative error banners (`[-] Error: Input audio file not found...`).
- **Smart Android `/tmp` Auto-Redirection**: Automatically detects read-only root `/tmp` access on non-root Android Termux and safely routes output files to `$TMPDIR` / `$HOME/tmp` with a polite notification, eliminating `PermissionError (Errno 13)`.
- **Pure-Python Speaker Diarization Fallback**: Integrated conversational turn-taking pause heuristics into `SpeakerMapper` to properly assign `Speaker_0` and `Speaker_1` even when external acoustic models are offline.

---

## 📋 Changelog

### ✨ Features & UX
- **`cli/main.py`**: Intercepts `FileNotFoundError`, `PermissionError`, and `ValueError` at the top level for clean terminal output.
- **`cli/transcribe.py` & `cli/diarize.py`**: Added `resolve_safe_output_path()` to transparently safeguard output paths on Android.
- **`diarization/mapper.py`**: Auto-assigns turn-taking speaker clusters during offline fallback.

### ✨ Features
- **`EngineInstaller._download_prebuilt_whisper`**: Added 1-second direct download pipeline for pre-compiled ARM64 Bionic whisper.cpp binaries from GitHub Releases.
- **`Manual Installation Manual`**: Added explicit instructions and curl one-liners for direct binary downloads.

### ⚡ Performance & Optimization
- **`Zero-Compilation Setup`**: Reduces default installation time on mobile Termux from ~2 minutes to under 2 seconds.
- **`On-Demand Toolchain Installation`**: Defers heavy `clang`, `cmake`, and `make` package installation strictly to the offline compilation fallback path.

### 🐛 Bug Fixes
- **`Permission & Overreach`**: Removed `su -c dumpsys` calls from `platform/mobile_guard.py`, ensuring graceful degradation on standard non-root Termux installations.
- **`Export Formats`**: Strengthened directory existence checks when writing SRT, VTT, and JSON export formats.

### ⚡ Performance & Security
- **`Zero-Network Error Path`**: Model lookup typos resolve locally in 0ms without hitting remote Hugging Face endpoints.
- **`OpenSSF Compliance`**: Enforced strict resource boundaries (`SAFE_SELF_SCOPED`), preventing execution of elevated system-wide routines.

---

## 📦 Package Distribution Details

| Platform | Package Identifier | Install Command | Verification Status |
| :--- | :--- | :--- | :---: |
| **PyPI (Python)** | `termux-stt` | `pip install termux-stt` | Validated |
| **npm (Node.js)** | `termux-stt` | `npm install termux-stt` | Validated |
