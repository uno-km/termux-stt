#!/data/data/com.termux/files/usr/bin/bash
set -e

echo "Installing whisper.cpp dependencies..."
pkg install -y cmake make git clang

git clone https://github.com/ggml-org/whisper.cpp.git /tmp/whisper.cpp || true
cd /tmp/whisper.cpp

echo "Building whisper.cpp with NEON..."
cmake -B build -DWHISPER_NEON=ON -DCMAKE_BUILD_TYPE=Release
cmake --build build -j$(nproc)

mkdir -p ~/.local/bin
cp build/bin/main ~/.local/bin/whisper-cpp
echo "whisper.cpp installed to ~/.local/bin/whisper-cpp"
