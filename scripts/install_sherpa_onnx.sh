#!/data/data/com.termux/files/usr/bin/bash
set -e

echo "Installing sherpa-onnx..."
mkdir -p ~/.local/bin
# Mocking the installation of aarch64 binary
touch ~/.local/bin/sherpa-onnx-offline
chmod +x ~/.local/bin/sherpa-onnx-offline
echo "sherpa-onnx mock installed to ~/.local/bin/sherpa-onnx-offline"
