# Termux-STT (Python)

[![PyPI](https://img.shields.io/pypi/v/termux-stt.svg?style=flat-square&color=0369a1)](https://pypi.org/project/termux-stt/)
[![Python](https://img.shields.io/pypi/pyversions/termux-stt.svg?style=flat-square)](https://pypi.org/project/termux-stt/)
[![License](https://img.shields.io/badge/License-Apache_2.0-004499.svg?style=flat-square)](https://github.com/uno-km/termux-stt)

> Unified On-Device Speech-to-Text & Neural Multi-Speaker Diarization (PyAnnote 3.0 + CAM++ 192d + TS-VAD Overlap Resolver)

## Installation

```bash
pip install termux-stt
```

## Quickstart

```python
from termux_stt import create_engine

# 1. Initialize Whisper Engine with Vulkan GPU / CPU Hybrid Acceleration
engine = create_engine("whisper", model="small", lang="ko", threads=4, split_mode=True)

# 2. Transcribe Audio directly into Subtitles
result = engine.transcribe("samples/jfk_1min.wav")
print("Transcript:\n", result.text)
print("SRT Subtitles:\n", result.to_srt())

# 3. Multi-Speaker Neural Diarization (PyAnnote 3.0 + CAM++ 192d + TS-VAD)
hybrid = create_engine("hybrid", lang="ko", num_speakers=2)
diar_result = hybrid.diarize("samples/kor_영어로화자분리.wav")
for seg in diar_result.segments:
    print(f"[{seg.speaker}] ({seg.start:.1f}s -> {seg.end:.1f}s): {seg.text}")

```

## Description
Integrates Whisper.cpp (Native Vulkan GPU / NEON CPU) and Sherpa-ONNX with PyAnnote 3.0 neural segmentation, 3D-Speaker CAM++ 192-dim embeddings, and TS-VAD overlapped speech resolution with zero cloud egress.

## Documentation
- [Official Documentation & API Reference](https://uno-km.vercel.app/lib/stt/)
- [GitHub Repository](https://github.com/uno-km/termux-stt)

## License
Apache-2.0 License. Copyright (c) 2026 Eunho Kim (@uno-km).
