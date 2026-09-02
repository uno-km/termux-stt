# termux-stt

> **On-Device Hybrid Speech-to-Text & Speaker Diarization Engine for Android Termux**  
> *Whisper.cpp · Vosk · Sherpa-ONNX · Non-Root ARM64 Execution · 128d Vector Diarization*

---

## ⚡ 5-Minute Quickstart

### Python Installation

`ash
# In Android Termux:
pkg update && pkg install -y python ffmpeg git
pip install termux-stt
`

### Python SDK Usage

`python
from termux_stt import STTEngine

engine = STTEngine(backend="whisper")
result = engine.transcribe("sample.wav")
print("Transcription:", result.text)
`

---

## 📚 Official Documentation

- **Official Web Documentation**: [https://uno-km.vercel.app/lib/stt/](https://uno-km.vercel.app/lib/stt/)
- **GitHub Repository**: [https://github.com/uno-km/termux-stt](https://github.com/uno-km/termux-stt)
- **License**: Apache-2.0