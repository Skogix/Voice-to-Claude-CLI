"""
Voice-to-Claude-CLI: Local voice transcription using whisper.cpp

This package provides cross-platform voice transcription capabilities with
three modes of operation:
- Daemon mode (voice_holdtospeak.py): F12 hold-to-speak with auto-paste
- One-shot mode (voice_to_text.py): Single transcription for hotkey binding
- Interactive mode (voice_to_claude.py): Terminal-based testing interface

Core components:
- VoiceTranscriber: Audio recording and transcription via whisper.cpp
- platform_detect: Cross-platform abstraction for clipboard/keyboard/notifications
"""

from .voice_to_claude import VoiceTranscriber
from .platform_detect import get_platform_info, PlatformInfo

__all__ = [
    'VoiceTranscriber',
    'get_platform_info',
    'PlatformInfo',
]
