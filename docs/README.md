# Voice-to-Claude-CLI

Local voice transcription for Claude Code using whisper.cpp. 100% private - no API keys or cloud services required.

> **🎤 QUICK START:** After installation, just press and hold **F12** to speak anywhere on your system!

## Installation

### Quick Install (2 steps)

**1. Add the plugin in Claude Code:**
```bash
/plugin add aldervall/Voice-to-Claude-CLI
```

**2. Run the installer:**
```bash
/voice-install
```

That's it! The installer handles everything automatically.

## Usage

### 🎯 Primary Method: Hold F12 to Speak

**Press and hold F12 anywhere on your system to transcribe voice to text:**

1. **Press and hold F12** - You'll hear a beep, recording starts
2. **Speak clearly** - Say what you want to transcribe
3. **Release F12** - Automatically transcribes and pastes into active window

**Works everywhere:**
- ✅ Claude Code chat window
- ✅ VS Code editor
- ✅ Terminal windows
- ✅ Web browsers
- ✅ Any text field in any application

**No need to switch windows or run commands - just hold F12 and speak!**

### Alternative Methods

**Voice Input in Claude Conversations:**
Simply say "record my voice" or "let me speak" to Claude, and it will autonomously activate voice transcription.

**Quick Command:**
Type `/voice` in Claude Code for quick voice input directly in the chat.

### First-Time Setup Note

After running `/voice-install`, the installer will:
- Install system dependencies (Python packages, audio tools)
- Download the whisper.cpp model (~142 MB, one-time)
- Set up the F12 hotkey daemon
- Configure auto-paste and notifications

**The first model download takes ~30 seconds. After that, transcription is instant!**

## What is This?

Voice-to-Claude-CLI is a **completely local** voice transcription system for Linux. Unlike cloud-based solutions:

- 🔒 **100% Private** - Your voice never leaves your computer
- 🔑 **No API Keys** - No cloud services, no accounts, no sign-ups
- ⚡ **Fast** - Uses optimized whisper.cpp for efficient local processing
- 📦 **Self-Contained** - Everything bundled, works offline
- 🎯 **System-Wide** - F12 hotkey works in every application

## Features

### Three Modes of Operation

**1. 🎤 Hold-to-Speak Daemon (Recommended)**
- Always-on F12 hotkey system-wide
- Hold to record, release to transcribe and paste
- Desktop notifications show transcription
- Works in any application

**2. 🗣️ Claude Voice Skill**
- Say "record my voice" to Claude
- Autonomous voice transcription in conversations
- Zero configuration needed
- Auto-discovered by Claude Code

**3. ⚡ Quick Voice Command**
- Use `/voice` in Claude Code
- Fast voice input directly in chat
- Great for quick messages

### Technical Features

- **🐧 Linux Support** - Arch, Ubuntu, Fedora, OpenSUSE (and derivatives)
- **🖥️ Multi-Environment** - Wayland & X11, KDE & GNOME & XFCE & i3 & Sway & more
- **⚡ Quick Setup** - Pre-built x64 binary, installs in 5 seconds (no compilation)
- **📦 Self-Contained** - whisper.cpp bundled in project, survives reboots
- **🤖 Claude Integration** - Auto-discovered Skill + slash commands
- **🛡️ Privacy First** - All processing happens locally on your machine

## Platform Support

**Operating Systems:**
- Arch Linux
- Ubuntu / Debian
- Fedora
- OpenSUSE
- Most Linux distributions

**Display Servers:**
- X11 (traditional)
- Wayland (modern)

**Desktop Environments:**
- KDE Plasma
- GNOME
- XFCE
- Cinnamon
- i3 / Sway (tiling window managers)
- Most desktop environments

**Requirements:**
- Python 3.8 or higher
- Working microphone (USB or built-in)
- Linux system with X11 or Wayland

## Troubleshooting

### F12 Hotkey Not Working?

**Check if the daemon is running:**
```bash
systemctl --user status voiceclaudecli-daemon
```

**Start the daemon manually:**
```bash
systemctl --user start voiceclaudecli-daemon
```

**Enable auto-start on login:**
```bash
systemctl --user enable voiceclaudecli-daemon
```

### No Audio Detected?

**Check microphone permissions:**
```bash
python -c "import sounddevice as sd; print(sd.query_devices())"
```

**Test voice transcription manually:**
```bash
voiceclaudecli-interactive
```

### Transcription Not Pasting?

**Check if ydotool is running (Wayland) or xdotool is installed (X11):**
```bash
systemctl --user status ydotool  # For Wayland
which xdotool  # For X11
```

**Restart the daemon after fixing dependencies:**
```bash
systemctl --user restart voiceclaudecli-daemon
```

### Still Having Issues?

See [CLAUDE.md](docs/CLAUDE.md) for comprehensive troubleshooting, development documentation, and detailed usage instructions.

## Advanced Usage

### Standalone Installation (Without Claude Code)

If you're not using Claude Code or want to install manually:

```bash
git clone https://github.com/aldervall/Voice-to-Claude-CLI
cd Voice-to-Claude-CLI
bash scripts/install.sh
```

### Command-Line Tools

After installation, these commands are available:

- `voiceclaudecli-daemon` - Start the F12 hold-to-speak daemon
- `voiceclaudecli-input` - One-shot voice input (types into active window)
- `voiceclaudecli-interactive` - Interactive terminal transcription mode

### Customization

Edit `~/.config/systemd/user/voiceclaudecli-daemon.service` to customize:
- Recording duration
- Audio beeps (enable/disable)
- Hotkey (change from F12 to another key)

After changes, reload the daemon:
```bash
systemctl --user daemon-reload
systemctl --user restart voiceclaudecli-daemon
```

## How It Works

**Voice-to-Claude-CLI uses:**
- **whisper.cpp** - Fast, efficient C++ implementation of OpenAI's Whisper model
- **Pre-built binary** - x64 binary included (no compilation needed)
- **ggml-base.en.bin model** - English-only, 142 MB, excellent accuracy
- **Local HTTP server** - whisper.cpp runs on localhost:2022
- **Python integration** - Clean Python interface for recording and transcription

**Data flow:**
1. Press F12 → Record audio via sounddevice
2. Send audio → whisper.cpp HTTP server (localhost only)
3. Transcribe → Get text response
4. Auto-paste → Insert into active window

**Nothing ever leaves your computer. No internet connection needed after installation.**

## Privacy & Security

- ✅ **100% Local Processing** - All transcription happens on your machine
- ✅ **No Cloud Services** - No API calls, no data sent to external servers
- ✅ **No API Keys** - No accounts, no sign-ups, no tracking
- ✅ **No Telemetry** - We don't collect any data or analytics
- ✅ **Open Source** - Full source code available for review
- ✅ **Works Offline** - No internet connection required after installation

Your voice is yours. It never leaves your computer.

## Documentation

- **[CLAUDE.md](docs/CLAUDE.md)** - Developer guide, architecture, troubleshooting
- **[HANDOVER.md](docs/HANDOVER.md)** - Development history and sessions
- **[docs/](docs/)** - Additional documentation

## Contributing

Contributions welcome! This project is open source.

## License

MIT License - see [LICENSE](LICENSE) for details.

## Support

- **Issues:** Report bugs at [GitHub Issues](https://github.com/aldervall/Voice-to-Claude-CLI/issues)
- **Documentation:** See [CLAUDE.md](docs/CLAUDE.md) for comprehensive guides
