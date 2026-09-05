# termux-stt

> **On-Device Hybrid Speech-to-Text & Speaker Diarization Engine for Android Termux**  
> *Whisper.cpp · Vosk · Sherpa-ONNX · Non-Root ARM64 Execution · 128d Vector Diarization*

---

## 5-Minute Quickstart

### Installation

```bash
# In Android Termux:
pkg update && pkg install -y python ffmpeg git
pip install --upgrade termux-stt
termux-stt install
```

### Instant CLI Demo

```bash
# Automatic benchmark audio download & transcription
termux-stt demo
```

### Python SDK Usage

```python
from termux_stt import create_engine

engine = create_engine("whisper", model="tiny", lang="en")
result = engine.transcribe("sample.wav")
print("Transcription:", result.text)
```

---

## 📚 Official Documentation

- **Official Web Documentation**: [https://uno-km.vercel.app/lib/stt/](https://uno-km.vercel.app/lib/stt/)
- **GitHub Repository**: [https://github.com/uno-km/termux-stt](https://github.com/uno-km/termux-stt)
- **License**: Apache-2.0