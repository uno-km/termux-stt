# termux-stt

> **Production-Grade On-Device Speech-to-Text & Speaker Diarization Framework for Node.js on Android Termux.**

<p align="center">
  <a href="https://www.npmjs.com/package/termux-stt"><img src="https://img.shields.io/npm/v/termux-stt.svg?style=flat-square&color=cb3837&logo=npm&logoColor=white" alt="npm Version" /></a>
  <a href="https://www.npmjs.com/package/termux-stt"><img src="https://img.shields.io/badge/npm%20Downloads-active-cb3837?style=flat-square&logo=npm&logoColor=white" alt="npm Downloads" /></a>
  <a href="https://github.com/uno-km/termux-stt/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-Apache%202.0-blue.svg?style=flat-square" alt="License" /></a>
  <img src="https://img.shields.io/badge/Platform-Android%20Termux%20(ARM64)-00887A?style=flat-square&logo=android&logoColor=white" alt="Platform" />
</p>

---

## 1. Quick Start

### 1.1 Installation

#### 1-Click Automated Setup:
```bash
pkg update -y && pkg install nodejs-lts ffmpeg git -y
npm install -g termux-stt
termux-stt install
```

#### Manual Pre-Compiled Binary Download (Direct GitHub Release):
```bash
mkdir -p ~/.local/bin
curl -sL "https://github.com/uno-km/termux-stt/releases/download/v1.1.1/whisper-cli-arm64-android" -o ~/.local/bin/whisper-cli
chmod 755 ~/.local/bin/whisper-cli
ln -sf ~/.local/bin/whisper-cli ~/.local/bin/whisper-cpp
export PATH=$HOME/.local/bin:$PATH
```

### 1.2 CLI Usage & Instant Sample Test

`termux-stt` includes a 60-second JFK inaugural address speech (`samples/jfk_1min.wav`) for immediate testing:

```bash
# 1. Transcribe sample speech with Whisper Tiny (Generates SRT subtitles)
termux-stt transcribe samples/jfk_1min.wav --engine whisper --model tiny --format srt

# 2. Transcribe with 128d Pure Python Speaker Diarization
termux-stt diarize samples/jfk_1min.wav --speakers 2
```

---

## 2. Programmatic Node.js API

```javascript
const { createEngine } = require('termux-stt');

async function main() {
  const engine = createEngine('whisper', { model: 'tiny', lang: 'en', threads: 4 });
  const result = await engine.transcribe('samples/jfk_1min.wav');
  console.log('Transcription:', result.text);
  console.log('SRT Subtitles:\n', result.toSrt());
}

main();
```

---

## 3. License

Apache License 2.0. Copyright (c) 2026 uno-km (AMEVA Foundation).\n