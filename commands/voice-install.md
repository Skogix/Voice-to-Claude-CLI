---
description: Install Voice-to-Claude-CLI with automated setup for your system
---

You are helping the user install Voice-to-Claude-CLI, a local voice transcription tool.

## Steps

1. **Verify we're in the project directory:**
   ```bash
   pwd  # Should be voiceclaudecli project
   ```

2. **Run installer:**
   ```bash
   bash scripts/install.sh
   ```
   - Auto-detects distro (Arch/Ubuntu/Fedora/OpenSUSE)
   - Installs dependencies (ydotool, clipboard tools)
   - Sets up Python venv
   - Creates launchers in ~/.local/bin
   - Installs systemd service
   - If prompted about whisper.cpp: Recommend **Yes**
   - If prompted about auto-start: Recommend **Yes**

3. **Important: If user added to 'input' group:**
   - User MUST log out and log back in for group changes to take effect

4. **Verify installation:**
   ```bash
   command -v voiceclaudecli-daemon
   curl http://127.0.0.1:2022/health
   ```

5. **Test daemon:**
   ```bash
   systemctl --user start voiceclaudecli-daemon
   systemctl --user status voiceclaudecli-daemon
   ```

## Usage Modes

- **Daemon (recommended):** Hold F12 to record, release to transcribe
- **One-shot:** Run `voiceclaudecli-input`
- **Interactive:** Run `voiceclaudecli-interactive`

## Notes

- Requires sudo for system packages
- All processing is local - no cloud services
- If installation fails, check error messages and see CLAUDE.md for manual steps
