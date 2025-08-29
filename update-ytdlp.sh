#!/bin/sh
set -e

echo "updating yt-dlp"
echo "killing youdis"
pkill -f youdis.py || true
python3 -m pip install --no-cache-dir --upgrade --pre "yt-dlp[default]"
VERSION=$(python3 -m pip show yt-dlp 2>/dev/null | awk '/Version:/ {print $2}')

echo "updated yt-dlp to $VERSION"
echo "restarting youdis"
python3 /app/youdis.py &
