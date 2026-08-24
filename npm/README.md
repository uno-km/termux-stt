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
  <a href="https://pypi.org/project/termux-stt/"><img src="https://img.shields.io/pypi/v/termux-stt.svg?style=for-the-badge&color=0088ff&logo=pypi&logoColor=white" alt="PyPI Version" /></a>
  <a href="https://pypi.org/project/termux-stt/"><img src="https://img.shields.io/badge/PyPI%20Downloads-active-0088ff?style=for-the-badge&logo=pypi&logoColor=white" alt="PyPI Downloads" /></a>
  <a href="https://www.npmjs.com/package/termux-stt"><img src="https://img.shields.io/npm/v/termux-stt.svg?style=for-the-badge&color=cb3837&logo=npm&logoColor=white" alt="npm Version" /></a>
  <a href="https://www.npmjs.com/package/termux-stt"><img src="https://img.shields.io/badge/npm%20Downloads-active-cb3837?style=for-the-badge&logo=npm&logoColor=white" alt="npm Downloads" /></a>
</p>

<p align="center">
  <a href="https://uno-km.vercel.app/lib/stt/"><img src="https://img.shields.io/badge/Official_Docs-uno--km.vercel.app%2Flib%2Fstt-004499?style=for-the-badge&logo=vercel&logoColor=white" alt="Live Docs" /></a>
  <a href="https://uno-km.vercel.app/lib/stt/demo.html"><img src="https://img.shields.io/badge/Live_Showcase-▶_Audio_Player-00f5d4?style=for-the-badge&logo=googlechrome&logoColor=0b132b" alt="Live Audio Showcase" /></a>
  <a href="https://github.com/uno-km/termux-stt"><img src="https://img.shields.io/github/stars/uno-km/termux-stt?style=for-the-badge&color=gold&logo=github" alt="GitHub Stars" /></a>
  <a href="https://github.com/uno-km/termux-stt/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-Apache%202.0-blue.svg?style=for-the-badge" alt="License" /></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Platform-Android%20Termux%20(ARM64%2Faarch64)-00887A?style=flat-square&logo=android&logoColor=white" alt="Platform" />
  <img src="https://img.shields.io/badge/Engines-whisper.cpp%20%7C%20Vosk%20%7C%20Sherpa--ONNX-38bdf8?style=flat-square" alt="Engines" />
  <img src="https://img.shields.io/badge/Diarization-128d%20X--Vector%20+%20Pure%20Python-a855f7?style=flat-square" alt="Diarization" />
  <img src="https://img.shields.io/badge/RAM-Under%20350MB%20(Tiny%2FBase)-10b981?style=flat-square&logo=shield&logoColor=white" alt="RAM" />
  <img src="https://img.shields.io/badge/Foundation-AOSF_Tier_1-orange?style=flat-square" alt="Foundation" />
</p>

<br/>

**[Live Audio Showcase & Demo](https://uno-km.vercel.app/lib/stt/demo.html)** • **[Official Documentation Site (13 Languages)](https://uno-km.vercel.app/lib/stt/)** • **[AMEVA Foundation](https://uno-km.vercel.app/docs/foundation/)** • **[Quickstart](#1-quick-scenario-playbook)** • **[Architecture](#2-why-termux-stt-architectural-pillars)** • **[Benchmarks](#3-empirical-benchmarks-galaxy-a35--exynos-1380)**

</div>

---

## AMEVA Foundation — Mobile AI Ecosystem

> **"$0 Cloud Egress, 0% External Data Leaks. Transforming every smartphone into an independent on-device AI workstation."**
> 
> The **AMEVA Open-Source Foundation (AOSF)** builds next-generation, client-centric AI runtimes spanning on-device large models, browser automation, neural network training, and speaker diarization.

<div align="center">

| Project | Platform & Packages | Core Capability & Technology | Documentation & Demo |
| :--- | :--- | :--- | :---: |
| **[termux-stt](https://github.com/uno-km/termux-stt)** | [![PyPI](https://img.shields.io/pypi/v/termux-stt?color=blue&style=flat-square)](https://pypi.org/project/termux-stt/) [![npm](https://img.shields.io/npm/v/termux-stt?color=red&style=flat-square)](https://www.npmjs.com/package/termux-stt) | **Integrated On-Device STT & Pure Python 128d X-Vector Diarization** (Whisper + Vosk + Sherpa) | **[Showcase](https://uno-km.github.io/termux-stt/showcase.html)** |
| **[termux-diffusion](https://github.com/uno-km/termux-diffusion)** | [![PyPI](https://img.shields.io/pypi/v/termux-diffusion?color=blue&style=flat-square)](https://pypi.org/project/termux-diffusion/) [![npm](https://img.shields.io/npm/v/termux-diffusion?color=red&style=flat-square)](https://www.npmjs.com/package/termux-diffusion) | **Mobile On-Device Stable Diffusion Image Generation** (bfloat16 ARM NEON acceleration) | **[Docs](https://uno-km.github.io/termux-diffusion/)** |
| **[termux-playwright](https://github.com/uno-km/termux-playwright)** | [![PyPI](https://img.shields.io/pypi/v/termux-playwright?color=blue&style=flat-square)](https://pypi.org/project/termux-playwright/) [![npm](https://img.shields.io/npm/v/termux-playwright?color=red&style=flat-square)](https://www.npmjs.com/package/termux-playwright) | **Non-Root Native Headless Chromium Browser Automation & Scraping** | **[Docs](https://uno-km.github.io/termux-playwright/)** |
| **[termux-train](https://github.com/uno-km/termux-train)** | [![PyPI](https://img.shields.io/pypi/v/termux-train.svg?color=blue&style=flat-square)](https://pypi.org/project/termux-train/) | **Mobile Native Autograd Neural Network Training & LoRA Fine-Tuning** | **[Docs](https://uno-km.vercel.app/lib/train/)** |

</div>

---

## 1. Quick Scenario Playbook

### Installation

#### Python SDK:
```bash
pkg update -y && pkg install python ffmpeg git -y
pip install termux-stt && termux-stt install
```

#### Node.js / TypeScript:
```bash
pkg update -y && pkg install nodejs-lts ffmpeg git -y
npm install -g termux-stt && npx termux-stt install
```

---

## License

Apache License 2.0. Copyright (c) 2026 uno-km (AMEVA Foundation).
