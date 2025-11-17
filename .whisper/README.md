# whisper.cpp Integration Directory

This directory contains the self-contained whisper.cpp installation for Voice-to-Claude-CLI.

## Directory Structure

```
.whisper/
├── bin/                    # Pre-built whisper-server binaries
│   ├── whisper-server-linux-x64
│   └── whisper-server-linux-arm64
├── models/                 # Whisper models (downloaded on first use)
│   └── ggml-base.en.bin   (142 MB, downloaded by install.sh)
└── scripts/               # Helper scripts
    ├── download-model.sh  # Download whisper model
    ├── start-server.sh    # Start local whisper server
    └── install-binary.sh  # Fallback: build from source
```

## Why This Directory Exists

Moving whisper.cpp into the project provides several benefits:
- **No compilation needed** - Pre-built binaries eliminate 5-minute build step
- **Self-contained** - Everything in one place, survives reboots
- **Auto-start capable** - Claude Code skill can start server automatically
- **Faster installation** - `git clone` → `bash install.sh` → done (< 5 seconds)

## Binaries

The `bin/` directory contains pre-built `whisper-server` binaries for:
- **linux-x64** - Standard 64-bit Intel/AMD processors (95% of users)
- **linux-arm64** - ARM64 processors (Raspberry Pi 4+, etc.)

These binaries are statically linked and should work on any modern Linux distribution.

## Models

Models are downloaded on first use to keep the repository size small:
- **base.en** (142 MB) - Default, good balance of speed/accuracy
- **tiny** (75 MB) - Fastest, lower accuracy
- **small** (466 MB) - Better accuracy, slower

The install script downloads base.en by default. You can download others:
```bash
bash .whisper/scripts/download-model.sh tiny
bash .whisper/scripts/download-model.sh small
```

## Usage

The whisper-server is automatically managed by:
- **install.sh** - Sets up systemd service
- **Skill script** - Auto-starts server if needed
- **Helper scripts** - Manual control

Manual start:
```bash
bash .whisper/scripts/start-server.sh
```

Check if running:
```bash
curl http://127.0.0.1:2022/health
```

## Fallback

If pre-built binaries don't work on your system:
```bash
bash .whisper/scripts/install-binary.sh
```

This builds whisper.cpp from source as a fallback.
