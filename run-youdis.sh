 #!/bin/sh
set -e

#start crond in bg
crond -l 2

echo "checking for /config/yt-dlp.conf"
#copy yt-dlp.conf if missing
mkdir -p /config
if [ ! -f /config/yt-dlp.conf ]; then
    echo "yt-dlp.conf not found, setting default"
    cp /app/default-yt-dlp.conf /config/yt-dlp.conf
    echo "created yt-dlp.conf"
fi

python3 -m pip install --no-cache-dir --upgrade --pre "yt-dlp[default]"
VERSION=$(python3 -m pip show yt-dlp 2>/dev/null | awk '/Version:/ {print $2}')
echo "updated yt-dlp to $VERSION"

echo "starting youdis"
exec python3 /app/youdis.py
