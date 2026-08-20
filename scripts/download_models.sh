#!/data/data/com.termux/files/usr/bin/bash
set -e

echo "Downloading models..."
# Mock model download
mkdir -p ~/.cache/termux_stt/models
echo "Mock model downloaded" > ~/.cache/termux_stt/models/whisper-tiny.txt
echo "Mock model downloaded" > ~/.cache/termux_stt/models/vosk-small-ko.txt
echo "Mock model downloaded" > ~/.cache/termux_stt/models/silero-vad.txt
echo "Models downloaded."
