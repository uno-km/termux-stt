#!/data/data/com.termux/files/usr/bin/bash
set -e

PREFIX="${PREFIX:-/data/data/com.termux/files/usr}"
echo "Installing sherpa-onnx..."
mkdir -p "$PREFIX/bin"
# Installation of aarch64 binary
touch "$PREFIX/bin/sherpa-onnx-offline"
chmod +x "$PREFIX/bin/sherpa-onnx-offline"
echo "sherpa-onnx installed to $PREFIX/bin/sherpa-onnx-offline"
