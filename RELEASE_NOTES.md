# 📦 Termux-STT v1.1.0 Release Notes

**Release Date:** August 26, 2026  
**Artifact ID:** `termux-stt-1.1.0`  
**Compliance Standard:** OpenSSF Best Practices, SAFE_SELF_SCOPED, Android Non-Root Standard  

---

## 🚀 Key Highlights
- **Fuzzy Typo Suggestion & Model Discovery**: `difflib`-based model recommendations and immediate catalog guidance upon misspelled model identifiers, safely terminating execution without remote network overhead.
- **Output Directory Auto-Creation**: Recursive auto-creation of missing parent output directories (`os.makedirs(..., exist_ok=True)`) preventing unexpected `FileNotFoundError` issues during automated pipelines.
- **Privileged Escalation Elimination**: Completely eliminated unauthorized `su` root attempts in `mobile_guard.py` to strictly comply with non-rooted Android user-space standards.

---

## 📋 Changelog

### ✨ Features
- **`ModelHub.ensure_model`**: Intercepts uncataloged or misspelled model names (e.g. `tniyy`), terminating with clean error output and fuzzy matching suggestions instead of failing on 404 HTTP requests.
- **`CLI Transcribe & Diarize`**: Added automatic directory creation for output paths (`--output <path>`).

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
