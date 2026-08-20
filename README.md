# termux-stt

[![PyPI version](https://badge.fury.io/py/termux-stt.svg)](https://badge.fury.io/py/termux-stt)
[![npm version](https://badge.fury.io/js/termux-stt.svg)](https://badge.fury.io/js/termux-stt)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/release/python-380/)

Android on-device STT framework for Termux — unifying whisper.cpp, vosk, and sherpa-onnx.

## Introduction
`termux-stt` is designed specifically for Android Termux (e.g. Exynos 1380, ARM NEON).
It leverages pure Python for math operations (cosine similarity, K-Means) and isolates C++ STT engines via subprocesses, avoiding heavy ML dependencies.

## Installation
```bash
pip install termux-stt
```

## Quickstart

### Python
```python
import termux_stt
engine = termux_stt.create_engine("whisper", model="tiny")
result = engine.transcribe("audio.wav")
print(result.text)
```

### CLI
```bash
termux-stt transcribe audio.wav --engine whisper --model tiny
```

### Node.js
```javascript
const { createEngine } = require('termux-stt');
const engine = createEngine("whisper", { model: "tiny" });
engine.transcribe("audio.wav").then(res => console.log(res.text));
```

## Engine Comparison
| Feature | whisper.cpp | Vosk | sherpa-onnx |
|---------|-------------|------|-------------|
| Precision | High | Medium | Fast |
| Speed | Medium | Fast | Very Fast |
| Best For | Batch/Quality | Stream/Offline | Stream/Fast |

## Blog Series
Check out the deep dive on the development process at Eunho Kim's blog (Posts #467~#481).

## License
MIT License. Copyright (c) 2024-2026 Eunho Kim (@uno-km)

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
