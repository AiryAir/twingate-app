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

## Install

```bash
./install.sh
```

This adds **Twingate Tray** to your app launcher by installing a `.desktop` file.

## Usage

```bash
python3 twingate-tray.py
```

Or launch **Twingate Tray** from your app launcher after installing.

## How It Works

The indicator checks `twingate status` for actual connection state and updates the tray icon accordingly. Connecting runs `twingate start` (which opens the browser for auth when needed), while disconnecting uses `pkexec twingate stop` for privilege escalation.
