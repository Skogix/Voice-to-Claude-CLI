#!/usr/bin/env python3
"""
Platform Detection Module
Detects Linux display server, desktop environment, and available tools
for cross-platform compatibility
"""
import os
import subprocess
import shutil
from typing import Dict, Optional, List


class PlatformInfo:
    """Container for platform detection results"""

    def __init__(self):
        self.display_server = self._detect_display_server()
        self.desktop_env = self._detect_desktop_environment()
        self.is_wayland = self.display_server == 'wayland'
        self.is_x11 = self.display_server == 'x11'
        self.is_kde = 'kde' in self.desktop_env.lower()
        self.is_gnome = 'gnome' in self.desktop_env.lower()

        # Detect available tools
        self.available_tools = self._detect_available_tools()

    def _detect_display_server(self) -> str:
        """Detect if running Wayland or X11"""
        # Check XDG_SESSION_TYPE first (most reliable)
        session_type = os.environ.get('XDG_SESSION_TYPE', '').lower()
        if session_type in ('wayland', 'x11'):
            return session_type

        # Check for Wayland display
        if os.environ.get('WAYLAND_DISPLAY'):
            return 'wayland'

        # Check for X11 display
        if os.environ.get('DISPLAY'):
            return 'x11'

        # Default assumption
        return 'unknown'

    def _detect_desktop_environment(self) -> str:
        """Detect desktop environment"""
        # Check XDG_CURRENT_DESKTOP (most common)
        desktop = os.environ.get('XDG_CURRENT_DESKTOP', '')
        if desktop:
            return desktop

        # Check DESKTOP_SESSION
        session = os.environ.get('DESKTOP_SESSION', '')
        if session:
            return session

        # Check for specific DE environment variables
        if os.environ.get('KDE_FULL_SESSION'):
            return 'KDE'
        if os.environ.get('GNOME_DESKTOP_SESSION_ID'):
            return 'GNOME'

        return 'unknown'

    def _detect_available_tools(self) -> Dict[str, List[str]]:
        """Detect which tools are available on the system"""
        tools = {
            'clipboard': [],
            'keyboard': [],
            'notification': []
        }

        # Clipboard tools
        if self._has_command('wl-copy') and self._has_command('wl-paste'):
            tools['clipboard'].append('wl-clipboard')
        if self._has_command('xclip'):
            tools['clipboard'].append('xclip')
        if self._has_command('xsel'):
            tools['clipboard'].append('xsel')

        # Keyboard automation tools
        if self._has_command('ydotool'):
            tools['keyboard'].append('ydotool')
        if self._has_command('kdotool'):
            tools['keyboard'].append('kdotool')
        if self._has_command('xdotool'):
            tools['keyboard'].append('xdotool')
        if self._has_command('wtype'):
            tools['keyboard'].append('wtype')

        # Notification tools
        if self._has_command('notify-send'):
            tools['notification'].append('notify-send')

        return tools

    def _has_command(self, cmd: str) -> bool:
        """Check if a command is available in PATH"""
        return shutil.which(cmd) is not None

    def get_clipboard_tool(self) -> Optional[str]:
        """Get the best clipboard tool for current environment"""
        if self.is_wayland and 'wl-clipboard' in self.available_tools['clipboard']:
            return 'wl-clipboard'
        elif self.is_x11:
            if 'xclip' in self.available_tools['clipboard']:
                return 'xclip'
            elif 'xsel' in self.available_tools['clipboard']:
                return 'xsel'
        elif 'wl-clipboard' in self.available_tools['clipboard']:
            # Fallback to wl-clipboard if available (works on some X11 setups)
            return 'wl-clipboard'

        return None

    def get_keyboard_tool(self) -> Optional[str]:
        """Get the best keyboard automation tool for current environment"""
        # Prefer ydotool as it works everywhere
        if 'ydotool' in self.available_tools['keyboard']:
            return 'ydotool'

        # KDE-specific fallback
        if self.is_kde and 'kdotool' in self.available_tools['keyboard']:
            return 'kdotool'

        # X11 fallback
        if self.is_x11 and 'xdotool' in self.available_tools['keyboard']:
            return 'xdotool'

        # Wayland compositor-specific (Sway, etc.)
        if self.is_wayland and 'wtype' in self.available_tools['keyboard']:
            return 'wtype'

        return None

    def copy_to_clipboard(self, text: str) -> bool:
        """Copy text to clipboard using best available tool"""
        clipboard_tool = self.get_clipboard_tool()

        if not clipboard_tool:
            return False

        try:
            if clipboard_tool == 'wl-clipboard':
                subprocess.run(['wl-copy', text], check=True, timeout=5)
            elif clipboard_tool == 'xclip':
                subprocess.run(
                    ['xclip', '-selection', 'clipboard'],
                    input=text.encode(),
                    check=True,
                    timeout=5
                )
            elif clipboard_tool == 'xsel':
                subprocess.run(
                    ['xsel', '--clipboard', '--input'],
                    input=text.encode(),
                    check=True,
                    timeout=5
                )
            else:
                return False

            return True
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
            return False

    def paste_from_clipboard(self) -> Optional[str]:
        """Paste text from clipboard using best available tool"""
        clipboard_tool = self.get_clipboard_tool()

        if not clipboard_tool:
            return None

        try:
            if clipboard_tool == 'wl-clipboard':
                result = subprocess.run(
                    ['wl-paste'],
                    capture_output=True,
                    text=True,
                    check=True,
                    timeout=5
                )
            elif clipboard_tool == 'xclip':
                result = subprocess.run(
                    ['xclip', '-selection', 'clipboard', '-o'],
                    capture_output=True,
                    text=True,
                    check=True,
                    timeout=5
                )
            elif clipboard_tool == 'xsel':
                result = subprocess.run(
                    ['xsel', '--clipboard', '--output'],
                    capture_output=True,
                    text=True,
                    check=True,
                    timeout=5
                )
            else:
                return None

            return result.stdout
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
            return None

    def type_text(self, text: str) -> bool:
        """Type text using best available keyboard automation tool"""
        keyboard_tool = self.get_keyboard_tool()

        if not keyboard_tool:
            return False

        try:
            if keyboard_tool == 'ydotool':
                # ydotool requires text to be typed character by character
                subprocess.run(['ydotool', 'type', text], check=True, timeout=10)
            elif keyboard_tool == 'kdotool':
                subprocess.run(['kdotool', 'type', text], check=True, timeout=10)
            elif keyboard_tool == 'xdotool':
                subprocess.run(['xdotool', 'type', '--', text], check=True, timeout=10)
            elif keyboard_tool == 'wtype':
                subprocess.run(['wtype', text], check=True, timeout=10)
            else:
                return False

            return True
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
            return False

    def simulate_paste_shortcut(self, use_shift: bool = False) -> bool:
        """
        Simulate paste keyboard shortcut (Ctrl+V or Shift+Ctrl+V)

        Args:
            use_shift: If True, use Shift+Ctrl+V (for terminals), else Ctrl+V (GUI apps)
        """
        keyboard_tool = self.get_keyboard_tool()

        if keyboard_tool != 'ydotool':
            # Only ydotool supports key simulation reliably
            return False

        try:
            if use_shift:
                # Shift+Ctrl+V for terminals
                # Key codes: 42=LeftShift, 29=LeftCtrl, 47=V
                subprocess.run(
                    ['ydotool', 'key', '42:1', '29:1', '47:1', '47:0', '29:0', '42:0'],
                    check=True,
                    timeout=2
                )
            else:
                # Ctrl+V for GUI apps
                # Key codes: 29=LeftCtrl, 47=V
                subprocess.run(
                    ['ydotool', 'key', '29:1', '47:1', '47:0', '29:0'],
                    check=True,
                    timeout=2
                )

            return True
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
            return False

    def get_install_instructions(self) -> str:
        """Get installation instructions for missing tools"""
        # Detect distribution
        distro = self._detect_distro()

        instructions = []

        # Check for missing clipboard tools
        clipboard_tool = self.get_clipboard_tool()
        if not clipboard_tool:
            if self.is_wayland:
                instructions.append(f"Install clipboard tool: {self._get_package_cmd(distro, 'wl-clipboard')}")
            else:  # X11
                instructions.append(f"Install clipboard tool: {self._get_package_cmd(distro, 'xclip')}")

        # Check for missing keyboard tools
        keyboard_tool = self.get_keyboard_tool()
        if not keyboard_tool:
            instructions.append(f"Install keyboard automation: {self._get_package_cmd(distro, 'ydotool')}")
            if keyboard_tool == 'ydotool':
                instructions.append("Enable ydotool daemon: systemctl --user enable --now ydotool")

        if not instructions:
            return "All required tools are installed!"

        return "\n".join(instructions)

    def _detect_distro(self) -> str:
        """Detect Linux distribution"""
        try:
            # Try to read /etc/os-release
            with open('/etc/os-release', 'r') as f:
                for line in f:
                    if line.startswith('ID='):
                        distro_id = line.split('=')[1].strip().strip('"').lower()
                        if distro_id in ('arch', 'manjaro', 'cachyos'):
                            return 'arch'
                        elif distro_id in ('ubuntu', 'debian', 'pop', 'mint'):
                            return 'debian'
                        elif distro_id in ('fedora', 'rhel', 'centos'):
                            return 'fedora'
                        elif distro_id in ('opensuse', 'sles'):
                            return 'opensuse'
        except FileNotFoundError:
            pass

        return 'unknown'

    def _get_package_cmd(self, distro: str, package: str) -> str:
        """Get package installation command for distro"""
        # Package name mappings for different distros
        package_names = {
            'wl-clipboard': {
                'arch': 'wl-clipboard',
                'debian': 'wl-clipboard',
                'fedora': 'wl-clipboard',
                'opensuse': 'wl-clipboard'
            },
            'xclip': {
                'arch': 'xclip',
                'debian': 'xclip',
                'fedora': 'xclip',
                'opensuse': 'xclip'
            },
            'ydotool': {
                'arch': 'ydotool',
                'debian': 'ydotool',
                'fedora': 'ydotool',
                'opensuse': 'ydotool'
            }
        }

        package_managers = {
            'arch': 'sudo pacman -S',
            'debian': 'sudo apt install',
            'fedora': 'sudo dnf install',
            'opensuse': 'sudo zypper install'
        }

        pkg_name = package_names.get(package, {}).get(distro, package)
        pkg_mgr = package_managers.get(distro, 'sudo <package-manager> install')

        return f"{pkg_mgr} {pkg_name}"

    def print_info(self):
        """Print detected platform information"""
        print("=" * 60)
        print("Platform Detection Results")
        print("=" * 60)
        print(f"Display Server: {self.display_server}")
        print(f"Desktop Environment: {self.desktop_env}")
        print(f"")
        print("Available Tools:")
        print(f"  Clipboard: {', '.join(self.available_tools['clipboard']) or 'None'}")
        print(f"  Keyboard: {', '.join(self.available_tools['keyboard']) or 'None'}")
        print(f"  Notification: {', '.join(self.available_tools['notification']) or 'None'}")
        print(f"")
        print("Selected Tools:")
        print(f"  Clipboard: {self.get_clipboard_tool() or 'None available'}")
        print(f"  Keyboard: {self.get_keyboard_tool() or 'None available'}")
        print("=" * 60)


# Global instance for easy access
_platform_info = None


def get_platform_info() -> PlatformInfo:
    """Get singleton PlatformInfo instance"""
    global _platform_info
    if _platform_info is None:
        _platform_info = PlatformInfo()
    return _platform_info


if __name__ == '__main__':
    # Test the detection when run directly
    platform = get_platform_info()
    platform.print_info()

    print("\nInstallation Instructions:")
    print(platform.get_install_instructions())
