#!/usr/bin/env bash
# Fallback: Build whisper-server from source if pre-built binary doesn't work

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BIN_DIR="$SCRIPT_DIR/../bin"
MODELS_DIR="$SCRIPT_DIR/../models"
BUILD_DIR="/tmp/whisper.cpp"

echo "Building whisper.cpp from source..."
echo "This requires: git, make, g++ or clang++"
echo ""

# Check for required tools
for cmd in git make; do
    if ! command -v "$cmd" &> /dev/null; then
        echo "Error: $cmd is required but not installed"
        echo ""
        echo "Install with:"
        echo "  Arch:   sudo pacman -S git make base-devel"
        echo "  Ubuntu: sudo apt install git make build-essential"
        echo "  Fedora: sudo dnf install git make gcc-c++"
        exit 1
    fi
done

# Clone and build
echo "Cloning whisper.cpp to $BUILD_DIR..."
if [ -d "$BUILD_DIR" ]; then
    echo "Directory exists, pulling latest..."
    cd "$BUILD_DIR"
    git pull
else
    git clone https://github.com/ggerganov/whisper.cpp "$BUILD_DIR"
    cd "$BUILD_DIR"
fi

echo "Building whisper-server..."
make clean
make -j$(nproc) server

# Copy binary
ARCH=$(uname -m)
case "$ARCH" in
    x86_64)
        TARGET="$BIN_DIR/whisper-server-linux-x64"
        ;;
    aarch64|arm64)
        TARGET="$BIN_DIR/whisper-server-linux-arm64"
        ;;
    *)
        echo "Warning: Unknown architecture $ARCH, using generic name"
        TARGET="$BIN_DIR/whisper-server"
        ;;
esac

echo "Copying binary to $TARGET..."
mkdir -p "$BIN_DIR"
cp "$BUILD_DIR/build/bin/whisper-server" "$TARGET"
chmod +x "$TARGET"

echo "✓ whisper-server built successfully"
ls -lh "$TARGET"

# Offer to download model
if [ ! -f "$MODELS_DIR/ggml-base.en.bin" ]; then
    echo ""
    echo "Model not found. Download now? [y/N]"
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        bash "$SCRIPT_DIR/download-model.sh" base.en
    else
        echo "You can download later with:"
        echo "  bash .whisper/scripts/download-model.sh base.en"
    fi
fi
