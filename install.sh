#!/bin/bash
set -euo pipefail

INSTALL_DIR="$(cd "$(dirname "$0")" && pwd)"
DESKTOP_DIR="$HOME/.local/share/applications"

mkdir -p "$DESKTOP_DIR"

cat > "$DESKTOP_DIR/twingate-tray.desktop" <<EOF
[Desktop Entry]
Type=Application
Name=Twingate Tray
Comment=Twingate VPN toggle for the system tray
Exec=python3 $INSTALL_DIR/twingate-tray.py
Icon=$INSTALL_DIR/icons/twingate-connected.svg
Terminal=false
Categories=Network;
StartupNotify=false
EOF

echo "Installed twingate-tray.desktop to $DESKTOP_DIR"
echo "You can now find 'Twingate Tray' in your app launcher."
