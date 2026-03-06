#!/usr/bin/python3
"""Twingate system tray indicator for Ubuntu — lightweight."""

import fcntl
import os
import sys
import subprocess
import gi

gi.require_version("Gtk", "3.0")
gi.require_version("AyatanaAppIndicator3", "0.1")
from gi.repository import Gtk, AyatanaAppIndicator3, GLib

POLL_INTERVAL_MS = 10_000
FAST_POLL_MS = 2_000
FAST_POLL_COUNT = 5
ICON_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icons")
LOCK_FILE = os.path.join(GLib.get_user_runtime_dir(), "twingate-tray.lock")


def is_active():
    """Check twingate service status via systemctl (no extra shell overhead)."""
    try:
        return subprocess.call(
            ["systemctl", "is-active", "-q", "twingate"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        ) == 0
    except FileNotFoundError:
        return False


class TwingateTray:
    def __init__(self):
        self.connected = is_active()
        self._fast_polls_left = 0
        self._poll_source = None

        self.indicator = AyatanaAppIndicator3.Indicator.new(
            "twingate-tray",
            self._icon_name(),
            AyatanaAppIndicator3.IndicatorCategory.APPLICATION_STATUS,
        )
        self.indicator.set_icon_theme_path(ICON_DIR)
        self.indicator.set_status(AyatanaAppIndicator3.IndicatorStatus.ACTIVE)

        self._build_menu()
        self._schedule_poll(POLL_INTERVAL_MS)

    def _icon_name(self):
        return "twingate-connected" if self.connected else "twingate-disconnected"

    def _build_menu(self):
        menu = Gtk.Menu()

        self.status_item = Gtk.MenuItem(label=self._status_label())
        self.status_item.set_sensitive(False)
        menu.append(self.status_item)

        menu.append(Gtk.SeparatorMenuItem())

        self.toggle_item = Gtk.MenuItem(label=self._toggle_label())
        self.toggle_item.connect("activate", self._on_toggle)
        menu.append(self.toggle_item)

        menu.append(Gtk.SeparatorMenuItem())

        quit_item = Gtk.MenuItem(label="Quit")
        quit_item.connect("activate", self._on_quit)
        menu.append(quit_item)

        menu.show_all()
        self.indicator.set_menu(menu)

    def _status_label(self):
        return "Twingate: Connected" if self.connected else "Twingate: Disconnected"

    def _toggle_label(self):
        return "Disconnect" if self.connected else "Connect"

    def _refresh_ui(self):
        self.indicator.set_icon_full(self._icon_name(), "Twingate")
        self.status_item.set_label(self._status_label())
        self.toggle_item.set_label(self._toggle_label())

    def _schedule_poll(self, interval):
        if self._poll_source is not None:
            GLib.source_remove(self._poll_source)
        self._poll_source = GLib.timeout_add(interval, self._poll_status)

    def _on_toggle(self, _widget):
        cmd = "stop" if self.connected else "start"
        subprocess.Popen(
            ["pkexec", "twingate", cmd],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        # Switch to fast polling briefly to pick up the change quickly
        self._fast_polls_left = FAST_POLL_COUNT
        self._schedule_poll(FAST_POLL_MS)

    def _poll_status(self):
        new_state = is_active()
        if new_state != self.connected:
            self.connected = new_state
            self._refresh_ui()

        if self._fast_polls_left > 0:
            self._fast_polls_left -= 1
            if self._fast_polls_left == 0:
                # Back to slow polling
                self._schedule_poll(POLL_INTERVAL_MS)
                return False
        return True

    def _on_quit(self, _widget):
        Gtk.main_quit()


def ensure_single_instance():
    lock_fd = open(LOCK_FILE, "w")
    try:
        fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        sys.exit(0)
    return lock_fd


def main():
    _lock = ensure_single_instance()
    TwingateTray()
    Gtk.main()


if __name__ == "__main__":
    main()
