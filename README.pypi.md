# Termux-STT (Python)

[![PyPI](https://img.shields.io/pypi/v/termux-stt.svg?style=flat-square&color=0369a1)](https://pypi.org/project/termux-stt/)
[![Python](https://img.shields.io/pypi/pyversions/termux-stt.svg?style=flat-square)](https://pypi.org/project/termux-stt/)
[![License](https://img.shields.io/badge/License-Apache_2.0-004499.svg?style=flat-square)](https://github.com/uno-km/termux-stt)

> Unified On-Device Speech-to-Text Utilizing Device Resources & Pure Python 128d X-Vector Speaker Diarization

## Installation

```bash
pip install termux-stt
```

## Quickstart

```python
from termux_stt import create_engine

# 1. Initialize Engine with Hybrid GPU-Encoder / CPU-Decoder Acceleration
engine = create_engine("whisper", model="small", lang="en", threads=4, split_mode=True)

# 2. Transcribe Audio directly into Subtitles
result = engine.transcribe("samples/jfk_1min.wav")
print("Transcript:\n", result.text)
print("SRT Subtitles:\n", result.to_srt())

# 3. 2-Speaker Diarization without PyTorch
hybrid = create_engine("hybrid", lang="en", num_speakers=2)
diar_result = hybrid.diarize("samples/jfk_1min.wav")
for seg in diar_result.segments:
    print(f"[{seg.speaker}] ({seg.start:.1f}s -> {seg.end:.1f}s): {seg.text}")

```

## Description
Integrates Whisper.cpp, Vosk, and Sherpa-ONNX with a closed-form pure-Python 128-dimensional X-Vector clustering algorithm that operates in under 80MB RAM with zero cloud egress.

## Hybrid Performance Highlights (Galaxy S25 - Snapdragon 8 Elite)

- **Whisper Small (60s JFK Audio)**: **12.93s** wall-clock time (**21.0% faster than Pure GPU**, **16.5% faster than Pure CPU**).
- **Whisper Large-v3-Turbo**: **86.52s** wall-clock time (28.5s faster than Pure CPU), with zero host CPU load during the 80s audio encoding stage.
- Upstream PR submitted to `ggml-org/whisper.cpp` ([PR #4089](https://github.com/ggml-org/whisper.cpp/pull/4089)).

## Documentation
- [Official Documentation & API Reference](https://uno-km.vercel.app/lib/stt/)
- [GitHub Repository](https://github.com/uno-km/termux-stt)

## License
Apache-2.0 License. Copyright (c) 2026 Eunho Kim (@uno-km).
