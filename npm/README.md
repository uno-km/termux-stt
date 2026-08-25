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

```bash
pkg update -y && pkg install nodejs-lts ffmpeg git -y
npm install -g termux-stt
```

### 1.2 CLI Usage

```bash
# 1. Initialize native voice recognition engines
npx termux-stt install

# 2. Transcribe local audio file
npx termux-stt transcribe meeting.wav --engine whisper --model base

# 3. Transcribe with 128d Speaker Diarization
npx termux-stt diarize interview.wav
```

---

## 2. Programmatic Node.js API

```javascript
const { createSTTEngine } = require('termux-stt');

async function main() {
  const engine = createSTTEngine({ engine: 'whisper', model: 'base' });
  const result = await engine.transcribe('sample.wav');
  console.log('Transcription:', result.text);
}

main();
```

---

## 3. License

Apache License 2.0. Copyright (c) 2026 uno-km (AMEVA Foundation).\n