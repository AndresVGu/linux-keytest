"""Temporarily disable GNOME shortcuts (Super, PrtSc) during testing."""

import subprocess


class GnomeKeyGrabber:

    def __init__(self):
        self._saved = {}

    def grab(self):
        """Disable GNOME shortcuts that intercept Super and PrtSc."""
        targets = [
            ("org.gnome.mutter", "overlay-key", "''"),
            ("org.gnome.shell.keybindings", "screenshot", "[]"),
            ("org.gnome.shell.keybindings", "screenshot-window", "[]"),
            ("org.gnome.shell.keybindings", "show-screenshot-ui", "[]"),
            ("org.gnome.settings-daemon.plugins.media-keys", "screenshot", "''"),
            ("org.gnome.settings-daemon.plugins.media-keys", "screenshot-clip", "''"),
            ("org.gnome.settings-daemon.plugins.media-keys", "window-screenshot", "''"),
            ("org.gnome.settings-daemon.plugins.media-keys", "window-screenshot-clip", "''"),
            ("org.gnome.settings-daemon.plugins.media-keys", "area-screenshot", "''"),
            ("org.gnome.settings-daemon.plugins.media-keys", "area-screenshot-clip", "''"),
        ]
        for schema, key, disable_val in targets:
            original = self._get(schema, key)
            if original is not None:
                self._saved[(schema, key)] = original
                self._set(schema, key, disable_val)

    def release(self):
        """Restore all GNOME shortcuts to their original values."""
        for (schema, key), value in self._saved.items():
            self._set(schema, key, value)
        self._saved.clear()

    @staticmethod
    def _get(schema, key):
        try:
            r = subprocess.run(
                ["gsettings", "get", schema, key],
                capture_output=True, text=True, timeout=3,
            )
            return r.stdout.strip() if r.returncode == 0 else None
        except Exception:
            return None

    @staticmethod
    def _set(schema, key, value):
        try:
            subprocess.run(
                ["gsettings", "set", schema, key, value],
                capture_output=True, timeout=3,
            )
        except Exception:
            pass
