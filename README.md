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

## Asymmetric Hybrid Architecture Benchmark (Galaxy S25 - Snapdragon 8 Elite)

> **Test Audio**: JFK Inaugural Address (60.59s mono 16kHz WAV)  
> **Silicon**: Qualcomm Snapdragon 8 Elite (Adreno 830 GPU + Oryon CPU)

| Model | Pure CPU (4T) | Pure GPU (Vulkan) | Hybrid GPU-CPU (4T) | Hybrid Efficiency (1T) | Speedup / Advantage |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Whisper Tiny** | 4.59s | 9.56s | **4.38s** | 5.48s | **+4.6% vs CPU** (Dispatch overhead minimized) |
| **Whisper Small** | 15.48s | 16.36s | **12.93s** | 23.02s | **+21.0% vs GPU**, **+16.5% vs CPU** |
| **Large-v3-Turbo** | 115.05s | 87.87s | **86.52s** | 90.39s | **-28.5s vs CPU**, CPU Load 0% during 80s encode |

*Multi-SoC Verification: Tested across Qualcomm Adreno 830, ARM Mali-G78 (Galaxy S21), and ARM Mali-G77 (Galaxy S20).*  
*Upstream Contribution: Official PR submitted to `ggml-org/whisper.cpp` ([PR #4089](https://github.com/ggml-org/whisper.cpp/pull/4089)).*

---

## Installation & Quickstart

### Python (PyPI)
```bash
pip install termux-stt
```
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

### CLI Command Line Usage
```bash
# 1. High-Performance Hybrid Transcribe (Vulkan GPU Encoder + 4 CPU Threads Decoder)
termux-stt transcribe samples/jfk_1min.wav --model small --split-mode

# 2. Ultra-Low Power Background Transcribe (GPU Encoder + 1 CPU Thread Decoder)
termux-stt transcribe meeting.wav --model small --optimize-1

# 3. Force Pure CPU Execution
termux-stt transcribe samples/jfk_1min.wav --device cpu --threads 4
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
