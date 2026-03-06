# Twingate Tray

A lightweight system tray indicator for [Twingate](https://www.twingate.com/) on Ubuntu/Linux using GTK 3 and Ayatana AppIndicator.

## Features

- Shows connection status in the system tray (connected/disconnected icons)
- Start and stop Twingate directly from the tray menu
- Polls service status automatically with adaptive polling intervals
- Single-instance enforcement via file lock

## Dependencies

- Python 3
- GTK 3
- `gir1.2-ayatanaappindicator3-0.1`

## Usage

```bash
python3 twingate-tray.py
```

Or use the included desktop entry (`twingate-tray.desktop`) for autostart.

## How It Works

The indicator checks the `twingate` systemd service status and updates the tray icon accordingly. Toggling the connection uses `pkexec twingate start/stop` for privilege escalation.
