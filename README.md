# Termux-STT

[![PyPI](https://img.shields.io/pypi/v/termux-stt.svg?style=flat-square&color=0369a1)](https://pypi.org/project/termux-stt/)
[![Python](https://img.shields.io/pypi/pyversions/termux-stt.svg?style=flat-square)](https://pypi.org/project/termux-stt/)
[![npm](https://img.shields.io/npm/v/termux-stt.svg?style=flat-square&color=b91c1c)](https://www.npmjs.com/package/termux-stt)
[![npm downloads](https://img.shields.io/npm/dm/termux-stt.svg?style=flat-square&color=b91c1c)](https://www.npmjs.com/package/termux-stt)
[![License](https://img.shields.io/badge/License-Apache_2.0-004499.svg?style=flat-square)](https://github.com/uno-km/termux-stt)

> **디바이스 리소스를 활용한 통합 온디바이스 음성인식(STT) 및 순수 Python 128d X-Vector 화자 분리 프레임워크**  
> *Unified On-Device Speech-to-Text Utilizing Device Resources & Pure Python 128d X-Vector Speaker Diarization*

---

## Architecture & Overview

Whisper.cpp, Vosk, Sherpa-ONNX 3대 네이티브 엔진을 통합하고, 닫힌 형태 순수 Python 128차원 X-Vector 클러스터링을 결합하여 80MB 미만의 초경량 메모리로 100% 온디바이스 실시간 음성인식과 화자 분리를 구현합니다.

Integrates Whisper.cpp, Vosk, and Sherpa-ONNX with a closed-form pure-Python 128-dimensional X-Vector clustering algorithm that operates in under 80MB RAM with zero cloud egress.

---

## Installation & Quickstart

### Python (PyPI)
```bash
pip install termux-stt
```
```python
from termux_stt import create_engine

# 1. Initialize Engine (auto-loads native ARM NEON binary & cached model)
engine = create_engine("whisper", model="tiny", lang="en", threads=4)

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

### Node.js / TypeScript (npm)
```bash
npm install termux-stt
```
```typescript
const { createEngine } = require("termux-stt");

async function main() {
  // 1. Initialize Whisper Engine
  const engine = createEngine("whisper", { model: "tiny", lang: "en", threads: 4 });

  // 2. Transcribe Audio
  const result = await engine.transcribe("samples/jfk_1min.wav");
  console.log("Transcript:", result.text);
  console.log("SRT Subtitles:\n", result.toSrt());
}
main();

```

---

## Official Documentation & Benchmarks
- [Official Architecture & API Reference](https://uno-km.vercel.app/lib/stt/)
- [Ecosystem Metrics & Registry Stats](https://uno-km.vercel.app/foundation/metrics)
- [AMEVA Open-Source Foundation Portal](https://uno-km.vercel.app/foundation/index.html)

---

## License
Licensed under the Apache-2.0 License. Copyright (c) 2026 Eunho Kim ([@uno-km](https://github.com/uno-km)).
