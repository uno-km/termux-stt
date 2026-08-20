# Termux-STT

<div align="center">

```
 ████████╗███████╗██████╗ ███╗   ███╗██╗   ██╗██╗  ██╗      ███████╗████████╗████████╗
 ╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║   ██║╚██╗██╔╝      ██╔════╝╚══██╔══╝╚══██╔══╝
    ██║   █████╗  ██████╔╝██╔████╔██║██║   ██║ ╚███╔╝ █████╗███████╗   ██║      ██║   
    ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║   ██║ ██╔██╗ ╚════╝╚════██║   ██║      ██║   
    ██║   ███████╗██║  ██║██║ ╚═╝ ██║╚██████╔╝██╔╝ ██╗      ███████║   ██║      ██║   
    ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═╝      ╚══════╝   ╚═╝      ╚═╝   
```

**Production-Grade On-Device Speech-to-Text & Speaker Diarization Framework for Android Termux**  
*Dual-Engine Architecture (Python & Node.js / TypeScript) with Native Bionic ARM64 Acceleration & 0 PyTorch Dependency*

<p align="center">
  <a href="https://pypi.org/project/termux-stt/"><img src="https://img.shields.io/pypi/v/termux-stt.svg?style=for-the-badge&color=00f5d4&logo=pypi&logoColor=0b132b" alt="PyPI Version" /></a>
  <a href="https://pypi.org/project/termux-stt/"><img src="https://img.shields.io/pypi/dm/termux-stt?style=for-the-badge&color=004499&logo=pypi&logoColor=white&label=PyPI%20Downloads" alt="PyPI Downloads" /></a>
  <a href="https://pepy.tech/project/termux-stt"><img src="https://img.shields.io/pepy/dt/termux-stt?style=for-the-badge&color=10b981&logo=pypi&logoColor=white&label=Total%20Installs" alt="Total Installs" /></a>
  <a href="https://www.npmjs.com/package/termux-stt"><img src="https://img.shields.io/npm/v/termux-stt.svg?style=for-the-badge&color=cb3837&logo=npm&logoColor=white" alt="npm Version" /></a>
  <a href="https://www.npmjs.com/package/termux-stt"><img src="https://img.shields.io/npm/dm/termux-stt?style=for-the-badge&color=ff5722&logo=npm&logoColor=white&label=npm%20Downloads" alt="npm Downloads" /></a>
  <a href="https://www.npmjs.com/package/termux-stt"><img src="https://img.shields.io/npm/dt/termux-stt?style=for-the-badge&color=e91e63&logo=npm&logoColor=white&label=Total%20npm" alt="Total npm" /></a>
</p>

<p align="center">
  <a href="https://uno-km.github.io/termux-stt/showcase.html"><img src="https://img.shields.io/badge/Live_Showcase-▶_Audio_Player-00f5d4?style=for-the-badge&logo=googlechrome&logoColor=0b132b" alt="Live Audio Showcase" /></a>
  <a href="https://uno-km.github.io/termux-stt/"><img src="https://img.shields.io/badge/Docs-uno--km.github.io-004499?style=for-the-badge&logo=googlechrome&logoColor=white" alt="Live Docs" /></a>
  <a href="https://github.com/uno-km/termux-stt"><img src="https://img.shields.io/github/stars/uno-km/termux-stt?style=for-the-badge&color=gold&logo=github" alt="GitHub Stars" /></a>
  <a href="https://github.com/uno-km/termux-stt/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge" alt="License" /></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Platform-Android%20Termux%20(ARM64%2Faarch64)-00887A?style=flat-square&logo=android&logoColor=white" alt="Platform" />
  <img src="https://img.shields.io/badge/Engines-whisper.cpp%20%7C%20Vosk%20%7C%20Sherpa--ONNX-38bdf8?style=flat-square" alt="Engines" />
  <img src="https://img.shields.io/badge/Diarization-128d%20X--Vector%20+%20Pure%20Python-a855f7?style=flat-square" alt="Diarization" />
  <img src="https://img.shields.io/badge/RAM-Under%20350MB%20(Tiny%2FBase)-10b981?style=flat-square&logo=shield&logoColor=white" alt="RAM" />
  <img src="https://img.shields.io/badge/Python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-f59e0b?style=flat-square&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Node.js-16%20%7C%2018%20%7C%2020%20%7C%2022-3178c6?style=flat-square&logo=nodedotjs&logoColor=white" alt="Node" />
</p>

<br/>

**[🎧 Live Audio Showcase & Demo](https://uno-km.github.io/termux-stt/showcase.html)** • **[📖 Official Documentation Site](https://uno-km.github.io/termux-stt/)** • **[🌌 AMEVA Foundation](#-ameva-foundation--mobile-ai-ecosystem)** • **[⚡ Quickstart](#1-quick-scenario-playbook)** • **[🏛️ Architecture](#2-why-termux-stt-architectural-pillars)** • **[📊 Benchmarks](#3-empirical-benchmarks-galaxy-a35--exynos-1380)** • **[🔍 15-Part Blog Series](#7-15-part-empirical-research-blog-series)**

</div>

---

## 🌌 AMEVA Foundation — Mobile AI Ecosystem

> **"클라우드 구독료 0원, 데이터 외부 유출 0%. 모든 스마트폰을 완벽한 독립형 AI 워크스테이션으로."**
> 
> **AMEVA 재단(AMEVA Foundation)**은 안드로이드 모바일 환경에서 거대 AI 모델과 브라우저 자동화, 신경망 훈련, 화자 분리 음성인식을 100% 로컬 온디바이스로 구동하는 차세대 오픈소스 생태계를 구축합니다.

<div align="center">

| 프로젝트 (Project) | 플랫폼 & 패키지 | 핵심 기능 & 온디바이스 기술 | 공식 문서 & 데모 |
| :--- | :--- | :--- | :---: |
| 🎙️ **[termux-stt](https://github.com/uno-km/termux-stt)** | [![PyPI](https://img.shields.io/pypi/v/termux-stt?color=blue&style=flat-square)](https://pypi.org/project/termux-stt/) [![npm](https://img.shields.io/npm/v/termux-stt?color=red&style=flat-square)](https://www.npmjs.com/package/termux-stt) | **통합 온디바이스 STT & 순수 Python 128d X-Vector 화자 분리** (Whisper + Vosk + Sherpa) | **[Showcase](https://uno-km.github.io/termux-stt/showcase.html)** |
| 🎨 **[termux-diffusion](https://github.com/uno-km/termux-diffusion)** | [![PyPI](https://img.shields.io/pypi/v/termux-diffusion?color=blue&style=flat-square)](https://pypi.org/project/termux-diffusion/) [![npm](https://img.shields.io/npm/v/termux-diffusion?color=red&style=flat-square)](https://www.npmjs.com/package/termux-diffusion) | **모바일 온디바이스 Stable Diffusion 이미지 생성** (bfloat16 ARM NEON 가속) | **[Docs](https://uno-km.github.io/termux-diffusion/)** |
| 🌐 **[termux-playwright](https://github.com/uno-km/termux-playwright-demo)** | [![PyPI](https://img.shields.io/pypi/v/termux-playwright?color=blue&style=flat-square)](https://pypi.org/project/termux-playwright/) [![npm](https://img.shields.io/npm/v/termux-playwright?color=red&style=flat-square)](https://www.npmjs.com/package/termux-playwright) | **PRoot 없는 네이티브 헤드리스 Chromium 브라우저 자동화 & 스크래핑** | **[Docs](https://uno-km.github.io/termux-playwright-demo/)** |
| 🧠 **[termux-train](https://github.com/uno-km/termux-train)** | [![GitHub](https://img.shields.io/badge/GitHub-termux--train-black?style=flat-square&logo=github)](https://github.com/uno-km/termux-train) | **모바일 순수 C++ Autograd 신경망 역전파 훈련 & LoRA 미세조정** | **[Repo](https://github.com/uno-km/termux-train)** |
| 🖥️ **[AMEVA Workstation](https://github.com/uno-km/AMEVA-Workstation-Web)** | [![WebGPU](https://img.shields.io/badge/WebGPU-100%25_On--Device-00f5d4?style=flat-square)](https://ameva-workstation-web-core.vercel.app/) | **100% 브라우저 로컬 WebGPU 멀티모달 문서 지능 & 오피스 워크스페이스** | **[Live Demo](https://ameva-workstation-web-core.vercel.app/)** |
| ⚡ **[AMEVA-Forge](https://github.com/uno-km/ameva-forge)** | [![WebGPU](https://img.shields.io/badge/3D_Studio-WebGPU-purple?style=flat-square)](https://uno-km.github.io/ameva-forge/demo.html) | **실시간 3D 뉴럴 스튜디오 & WebGPU 비주얼라이제이션 엔진** | **[Live Demo](https://uno-km.github.io/ameva-forge/demo.html)** |

</div>

---

## 🎙️ 단 3줄로 끝내는 안드로이드 Termux 온디바이스 음성인식

```python
from termux_stt import create_engine

# 1. 엔진 초기화 (최초 1회 모델 자동 다운로드 및 캐싱)
engine = create_engine("whisper", model="base", lang="en")

# 2. 오디오 전사 및 자막 생성 (WAV, MP3, M4A, FLAC 등 자동 16kHz 변환)
result = engine.transcribe("speech.mp3")

print(result.text)          # 전체 텍스트
print(result.to_srt())       # 표준 SRT 자막
```

```bash
# 또는 터미널에서 1줄 CLI 실행
termux-stt transcribe --engine whisper --model base speech.mp3
```

---

## 🎧 Live Audio Showcase & On-Device Transcription Proof

> **[▶ 웹 브라우저에서 실시간 음성 및 동기화 자막 체험하기 (Live Audio Showcase)](https://uno-km.github.io/termux-stt/showcase.html)**

### 1. 실측 오디오 스펙 & 전사 타임라인

* **입력 오디오**: `continuous_speech.wav` (37.91초, 16000Hz Mono PCM)
* **추론 엔진**: `whisper.cpp Base` (On-Device Local CPU)
* **처리 시간**: **32.79초** (RTF: **0.865x**, 실시간보다 빠름)
* **문장 반복률**: **0%** (모든 발화 구간이 각기 다른 내용으로 고유하게 전사됨)

| No. | 타임스탬프 (시작 → 종료) | 전사된 문장 (Transcribed Text) |
| :---: | :---: | :--- |
| **01** | `00:00.00 → 00:09.36` | *"And so my fellow Americans, ask not what your country can do for you, ask what you can"* |
| **02** | `00:09.36 → 00:11.60` | *"do for your country."* |
| **03** | `00:11.60 → 00:16.18` | *He hoped there would be stew for dinner, turnips and carrots and bruised potatoes and* |
| **04** | `00:16.18 → 00:22.00` | *fat mutton pieces to be ladled out in thick, peppered flour-fatten sauce.* |
| **05** | `00:22.00 → 00:25.36` | *Stuff it into you, his belly counseled him.* |
| **06** | `00:25.36 → 00:29.88` | *After early nightfall, the yellow lamps would light up here and there, the squalid quarter* |
| **07** | `00:29.88 → 00:37.14` | *of the brothels.* |

### 2. 자동 생성된 SRT 자막 파일

```srt
1
00:00:00,000 --> 00:00:09,360
"And so my fellow Americans, ask not what your country can do for you, ask what you can

2
00:00:09,360 --> 00:00:11,600
do for your country."

3
00:00:11,600 --> 00:00:16,180
He hoped there would be stew for dinner, turnips and carrots and bruised potatoes and

4
00:00:16,180 --> 00:00:22,000
fat mutton pieces to be ladled out in thick, peppered flour-fatten sauce.

5
00:00:22,000 --> 00:00:25,360
Stuff it into you, his belly counseled him.

6
00:00:25,360 --> 00:00:29,880
After early nightfall, the yellow lamps would light up here and there, the squalid quarter

7
00:00:29,880 --> 00:00:37,140
of the brothels.
```

---

## 💡 What is termux-stt?

`termux-stt` is an all-in-one, production-ready speech-to-text and speaker diarization framework engineered natively for **Android Termux (ARM64 / aarch64)**.

Standard mobile STT setups force developers to endure 30+ minutes of manual CMake builds, broken PyPI wheels on Android Bionic, 2GB+ PyTorch binaries that trigger Android Low Memory Killer (OOM), and broken platform guards.

**`termux-stt` eliminates all friction with a 3-line unified API:**
- **Zero-PyTorch Dependency**: Replaces heavy ML frameworks with C++ binary subprocess isolation and Pure Python clustering math.
- **Multi-Engine Unification**: Run `whisper.cpp`, `Vosk`, or `Sherpa-ONNX` via the exact same `create_engine()` interface.
- **Built-in Hybrid Diarization**: Combines Vosk 128d X-Vector voice fingerprints with Whisper STT under 1.5 GB RAM.
- **Empirically Proven**: Engineered from 15 comprehensive benchmarks on Samsung Galaxy A35 (Exynos 1380, 6GB RAM).

---

## 1. Quick Scenario Playbook

### [Install] Scenario 1: Clean Install (Fresh Setup on Android Termux)

#### [Python] Python (`pip`):
```bash
# 1. Grant Storage & Microphone Permissions in Termux
termux-setup-storage

# 2. Install Dependencies & Provision Native Engines
pkg update -y && pkg install python clang make cmake git ffmpeg termux-api -y
pip install termux-stt && termux-stt-install
```

#### [Node.js] Node.js / TypeScript (`npm`):
```bash
# 1. Grant Storage & Microphone Permissions
termux-setup-storage

# 2. Install Dependencies & Provision Native Engines
pkg update -y && pkg install nodejs-lts clang make cmake git ffmpeg termux-api -y
npm install -g termux-stt && npx termux-stt install
```

---

### [Instant] Scenario 2: Instant Transcription (Ready to Run)

#### Option A: One-Line CLI
```bash
# Transcribe audio file with default Whisper engine (Korean)
termux-stt transcribe meeting.wav

# Export directly to Subtitles (SRT or VTT)
termux-stt transcribe --format srt meeting.wav > subtitles.srt

# Use ultra-fast Vosk engine
termux-stt transcribe --engine vosk --model small-ko voice_memo.wav
```

#### Option B: Python SDK Integration
```python
from termux_stt import create_engine

# 1. Initialize Engine (auto-downloads model on first call)
engine = create_engine("whisper", model="base", lang="ko")

# 2. Transcribe Audio
result = engine.transcribe("meeting.wav")

print("Transcript:", result.text)
print("Detected Language:", result.language)
print("Duration:", f"{result.duration:.2f}s")
```

#### Option C: Node.js / TypeScript Integration
```javascript
const { createEngine } = require("termux-stt");

async function main() {
  const engine = createEngine("whisper", { model: "base", lang: "ko" });
  const result = await engine.transcribe("meeting.wav");
  
  console.log("Transcript:", result.text);
  console.log("SRT Subtitles:\n", result.toSrt());
}
main();
```

---

### [Streaming] Scenario 3: Real-Time Microphone Streaming

Speak into your smartphone microphone and receive real-time transcribed text with sub-second latency:

```python
from termux_stt import create_engine

# Use ultra-lightweight Tiny model (RTF 0.80 on Exynos 1380)
engine = create_engine("whisper", model="tiny", lang="ko")

print("🎙️ Listening... Speak into your phone microphone (Ctrl+C to stop)")
for segment in engine.stream_mic():
    print(f"[{segment.start:.1f}s -> {segment.end:.1f}s] {segment.text}")
```

---

### [Diarize] Scenario 4: Hybrid Speaker Diarization ("Who Spoke When?")

Run high-precision speaker diarization without PyTorch or CUDA:

```python
from termux_stt import create_engine

# Hybrid Pipeline: Vosk 128d X-Vector + Whisper STT + Pure Python K-Means
engine = create_engine("hybrid", lang="ko", num_speakers=2)
result = engine.diarize("interview.wav")

for seg in result.segments:
    print(f"[{seg.speaker}] ({seg.start:.1f}s - {seg.end:.1f}s): {seg.text}")
```

*Output Example:*
```text
[Speaker_0] (0.0s - 3.5s): 오늘 경제 브리핑을 시작하겠습니다.
[Speaker_1] (3.8s - 7.2s): 네, 오늘 코스피 지수가 외국인 순매수로 상승 마감했습니다.
[Speaker_0] (7.5s - 10.1s): 반도체 섹터 동향은 어떤가요?
```

---

## 2. 🏛️ Why termux-stt? Architectural Pillars

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           termux-stt Architecture                          │
├────────────────────────┬────────────────────────┬───────────────────────────┤
│   User Interface Layer │   Engine Abstraction   │   Output / Export Layer   │
│  • Python API          │  • EngineRegistry      │  • JSON / SRT / VTT       │
│  • Node.js API         │  • create_engine()     │  • RTTM (Diarization)     │
│  • CLI (termux-stt)    │  • ModelHub & Cache    │  • Streaming Callback     │
├────────────────────────┼────────────────────────┼───────────────────────────┤
│                   Core Pipeline Layer                                       │
│  Audio Loader (7 Formats) ➔ Preprocessor (16kHz Mono) ➔ Silero-VAD Filter  │
│  ➔ Multi-Engine STT (whisper.cpp / Vosk / Sherpa-ONNX)                     │
│  ➔ Hybrid Diarizer (128d X-Vector ➔ Pure Python Cosine/K-Means ➔ Time Align)│
├─────────────────────────────────────────────────────────────────────────────┤
│                   Platform & Process Isolation                              │
│  • Subprocess Isolation (Host Python never crashes on C++ Segfault)         │
│  • MobileGuard (WakeLock, Doze Mode Bypass, Phantom Process Killer Shield)  │
│  • Bionic ARM64 NEON & FP16 SIMD Acceleration                               │
└─────────────────────────────────────────────────────────────────────────────┘
```

1. **Subprocess Isolation**: C++ inference runs in isolated native subprocesses. Memory errors or Segfaults never kill the host Python/Node.js application.
2. **Pure Python Clustering**: Cosine distance matrix and K-Means clustering are implemented with 0 external dependencies (`numpy` / `scikit-learn` optional, not required).
3. **Automated Android Bionic Fixes**: Solves `sys.platform = 'linux'` spoofing, libvosk CFFI extraction, and ffmpeg audio format normalization (`16kHz / 1ch / PCM s16le`) under the hood.
4. **Mobile Battery & CPU Guard**: Manages Android WakeLocks and background task states to prevent process termination when the screen locks.

---

## 3. 📊 Empirical Benchmarks (Galaxy A35 / Exynos 1380)

> *Measured on Samsung Galaxy A35 5G (Exynos 1380 4x A78 + 4x A55, 6GB RAM, Android 14 Termux).*

| Engine / Pipeline | Model | Peak RAM | RTF (Speed) | KO Accuracy | Diarization Support | Termux Rating |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **whisper.cpp** | `ggml-tiny` (39M) | **~150 MB** | **0.80** | 85% | ❌ External | ⭐⭐⭐⭐⭐ |
| **whisper.cpp** | `ggml-base` (74M) | ~250 MB | 1.20 | 88% | ❌ External | ⭐⭐⭐⭐ |
| **whisper.cpp** | `ggml-medium` (769M) | ~1.5 GB | 3.40 | **95%+** | ❌ External | ⭐⭐⭐ (Golden Acc) |
| **Vosk** | `small-ko-0.22` (42M) | **~100 MB** | **0.25** | 78% | ✅ 128d X-Vector | ⭐⭐⭐ |
| **Sherpa-ONNX** | `Zipformer` | ~300 MB | **0.42** | 86% | ✅ CAM++ | ⭐⭐⭐⭐ |
| **Pyannote.audio 3.1** | `diarization-3.1` | **> 3.5 GB** | 2.80~3.50 | N/A | ✅ Gold Standard | ❌ OOM Crashes |
| **termux-stt (Hybrid)** | `Vosk + Whisper Base`| **~350 MB** | **1.45** | **92%+** | **✅ Built-in K-Means** | **⭐⭐⭐⭐⭐ (Recommended)** |

---

## 4. ⚙️ Engine Comparison Matrix

| Feature | `whisper.cpp` | `Vosk` | `Sherpa-ONNX` | `Hybrid (Vosk+Whisper)` |
| :--- | :---: | :---: | :---: | :---: |
| **Primary Strength** | Highest Text Accuracy | Ultra-Low RAM & Fast | Ultra-Low Latency | **STT + Diarization Combined** |
| **Memory Footprint** | 150MB ~ 1.5GB | **< 100MB** | 300MB ~ 500MB | **~ 350MB** |
| **Real-Time Factor (RTF)** | 0.80 (Tiny) | **0.25 (Blazing)** | **0.42 (Fast)** | 1.45 (Full Pipeline) |
| **Speaker Diarization** | ❌ None | ⚠️ Basic X-Vector | ⚠️ CAM++ C++ | **✅ High-Precision Aligned** |
| **Recommended Use Case** | Quality Transcripts | Embedded / Low Spec | Live Voice Assistant | **Meetings / Interviews** |

---

## 5. 📚 Complete API Reference Summary

### Python API

```python
import termux_stt

# Create Engine with fine-grained control parameters
engine = termux_stt.create_engine(
    engine="whisper",         # "whisper" | "vosk" | "sherpa" | "hybrid"
    model="base",             # "tiny" | "base" | "small" | "medium" | "custom"
    lang="ko",                # ISO 639-1 language code
    num_speakers=0,           # 0 = disabled, 2+ = enable diarization
    threads=4,                # CPU threads (defaults to big cores count)
    vad=True,                 # Enable Silero-VAD silence stripping
    quantization="q5_1",      # "f16" | "q8_0" | "q5_1" | "q4_0"
    prompt="경제 브리핑",     # Initial decoding context / vocabulary
    beam_size=5,              # Beam search beam size
    temperature=0.0           # Sampling temperature
)

# Transcribe File
result = engine.transcribe("audio.wav")
# Returns: TranscriptResult(text=str, segments=List[Segment], language=str, duration=float)

# Export Methods
result.to_json()              # Structured JSON string
result.to_srt()               # Standard SRT subtitle format
result.to_vtt()               # WebVTT subtitle format
result.to_rttm()              # NIST RTTM diarization format

# Stream Microphone
for seg in engine.stream_mic(duration=30.0):
    print(f"[{seg.speaker}] {seg.text}")

# Speaker Diarization
diar_result = engine.diarize("meeting.wav", num_speakers=2)
```

### CLI Reference

```bash
# General Syntax
termux-stt [COMMAND] [OPTIONS] [FILE]

# Commands
termux-stt transcribe [FILE]   # Transcribe audio file (--prompt, --beam-size, --translate)
termux-stt listen              # Real-time microphone transcription
termux-stt diarize [FILE]      # Perform speaker diarization
termux-stt models list         # List installed and available models
termux-stt models download [M] # Download specific model
termux-stt doctor              # Run hardware and environment diagnostics
termux-stt benchmark           # Run performance benchmark suite
```

---

## 6. 🛠️ Troubleshooting & Android FAQs

### Q1: `pip install vosk` fails with CMake or wheel error on Android
* **Cause**: Vosk does not publish official prebuilt aarch64-android wheels on PyPI.
* **Solution**: `termux-stt-install` automatically extracts `libvosk.so` from the official Android AAR and generates the CFFI bindings.

### Q2: Whisper crashes on 44.1kHz stereo MP3/M4A files
* **Cause**: Whisper models strictly require single-channel 16,000Hz 16-bit PCM WAV.
* **Solution**: `termux-stt` automatically runs `ffmpeg` normalization on any audio format (`mp3`, `m4a`, `flac`, `ogg`, `opus`, `webm`).

### Q3: Process killed after 10 minutes in background
* **Cause**: Android Phantom Process Killer terminates background tasks.
* **Solution**: Enable Termux WakeLock (`termux-wake-lock`) and disable battery optimization for Termux in Android Settings.

---

## 7. 🔍 15-Part Empirical Research Blog Series

This framework is built upon the exhaustive 15-part research series published on [Eunho Kim's Technical Blog (우노킴 티스토리)](https://uno-kim.tistory.com/):

1. [[Whisper.cpp] #1. Edge Agent AI: Whisper.cpp Speech Processing (Base vs Tiny)](https://uno-kim.tistory.com/467)
2. [[Audio Extraction] #2. Extracting Specific Audio Segments on Android](https://uno-kim.tistory.com/468)
3. [[Whisper.cpp] #3. Korean STT Conversion Comparison (4 Models)](https://uno-kim.tistory.com/469)
4. [[Comparison-1] #4. STT + Speaker Diarization: 3 Lightweight Engines + Pyannote](https://uno-kim.tistory.com/472)
5. [[Comparison-2] #5. Sherpa-ONNX Execution, Diarization, and Troubleshooting](https://uno-kim.tistory.com/473)
6. [[Comparison-3] #6. Speaker Diarization using Pyannote Model](https://uno-kim.tistory.com/471)
7. [[Pyannote] Troubleshooting Diarization in Mobile/Termux/ARM Environments](https://uno-kim.tistory.com/470)
8. [[Comparison-4] #7. Vosk Execution, Speaker Diarization, and Troubleshooting](https://uno-kim.tistory.com/475)
9. [[Vosk] Troubleshooting Vosk in Mobile/Termux/ARM Environments](https://uno-kim.tistory.com/474)
10. [[Comparison-5] #8. Vosk / Pyannote / Sherpa-ONNX / Whisper.cpp Comprehensive Comparison](https://uno-kim.tistory.com/476)
11. [[Comparison-6] #9. Vosk + Whisper.cpp Hybrid Pipeline & X-Vector Diarization](https://uno-kim.tistory.com/477)
12. [[Development-1] #10. Large-Scale Batch Automation & Task Management Architecture](https://uno-kim.tistory.com/478)
13. [[Comparison-7] #11. STT + Diarization Final: Small vs Turbo & Optimization Magic (4-Model Benchmark)](https://uno-kim.tistory.com/479)
14. [[Development-2] #12. Domain-Specific STT Training: Whisper Tiny Fine-Tuning on CPU](https://uno-kim.tistory.com/480)
15. [[Comparison-8] #13. Vanilla Model vs Custom Fine-Tuned Model (Economics/News Domain)](https://uno-kim.tistory.com/481)

---

## ⚖️ Disclaimer (면책 조항)

> **Disclaimer:**  
> *termux-stt is an independent open-source project developed for the Android Termux environment and is not officially affiliated with, endorsed by, or sponsored by the Termux project, OpenAI, or any other third party.*  
> 
> *(본 프로젝트는 안드로이드 Termux 환경을 위해 개발된 독립적인 오픈소스 라이브러리이며, Termux 공식 프로젝트, OpenAI 및 기타 제3자와 직접적인 제휴 관계가 아닙니다.)*

---

## 📄 License

Released under the **MIT License**. Maintained by **AMEVA Foundation & uno-km (쌩초보코딩단) / Eunho Kim**.
