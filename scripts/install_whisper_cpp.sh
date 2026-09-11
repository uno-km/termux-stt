#!/data/data/com.termux/files/usr/bin/bash
set -e

echo "Installing whisper.cpp dependencies..."
pkg install -y cmake make git clang

git clone https://github.com/ggml-org/whisper.cpp.git /tmp/whisper.cpp || true
cd /tmp/whisper.cpp

# 1. Provision ameva-runtime
if command -v pip >/dev/null 2>&1; then
    pip install ameva-runtime || true
fi

# 2. Build whisper.cpp
cmake -B build -DWHISPER_NEON=ON -DGGML_VULKAN=ON -DCMAKE_BUILD_TYPE=Release 2>/dev/null || \
cmake -B build -DWHISPER_NEON=ON -DCMAKE_BUILD_TYPE=Release
cmake --build build -j$(nproc)

mkdir -p ~/.local/bin
cp build/bin/main ~/.local/bin/whisper-cpp 2>/dev/null || cp build/bin/whisper-cli ~/.local/bin/whisper-cli 2>/dev/null || true
echo "whisper.cpp installed to ~/.local/bin"
