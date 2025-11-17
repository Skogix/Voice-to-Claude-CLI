# Voice-to-Claude-CLI

Local voice transcription for Claude Code using whisper.cpp. 100% private - no API keys or cloud services required.

## Install in Claude Code

**1. Add the plugin:**
```bash
/plugin marketplace add aldervall/Voice-to-Claude-CLI
/plugin install voice-transcription@voice-to-claude-marketplace
```

**2. Run the installer:**
```bash
/voice-install
```

**3. Start using:**
- Say "record my voice" to Claude
- Or use `/voice` for quick voice input
- Or press F12 to hold-and-speak (daemon mode)

## Features

- **🌐 Cross-Platform** - Works on Arch, Ubuntu, Fedora, OpenSUSE
- **🖥️ Multi-Environment** - Supports Wayland & X11, KDE & GNOME & more
- **🔒 100% Local** - All processing happens on your machine
- **🔑 No API Keys** - No cloud services, no accounts needed
- **⚡ Fast Install** - Pre-built x64 binary included, no compilation needed (5 sec vs 5 min)
- **📦 Self-Contained** - whisper.cpp bundled in project, survives reboots
- **🎯 Three Modes**:
  - **Hold-to-Speak Daemon** - Always-on F12 hotkey (recommended)
  - **One-Shot Voice Input** - Quick voice input for typing into applications
  - **Interactive Mode** - Terminal-based transcription sessions
- **🛡️ Privacy First** - Your voice never leaves your computer
- **⚙️ Fast** - Uses whisper.cpp for efficient local transcription
- **🤖 Claude Integration** - Zero-config Skill with auto-start + slash commands for Claude Code

## Platform Support

**Supported:**
- **Linux:** Arch, Ubuntu, Fedora, OpenSUSE (and derivatives)
- **Display:** Wayland & X11
- **Desktop:** KDE, GNOME, XFCE, Cinnamon, i3, Sway, and more

**Prerequisites:**
- Python 3.8 or higher
- Working microphone
- Linux system

## Advanced

**Standalone installation (without Claude Code):**
```bash
bash scripts/install.sh
```

**Documentation:**
- See [CLAUDE.md](docs/CLAUDE.md) for development, troubleshooting, and detailed usage
- See [docs/](docs/) for additional documentation

## Privacy & Security

All voice processing happens completely locally on your machine. Your audio never leaves your computer, no API keys needed, no telemetry, no cloud services.

## License

MIT License - see [LICENSE](LICENSE) for details.

## Author

Niklas Aldervall (niklas@aldervall.se)
