#!/bin/sh
#copy yt-dlp.conf if missing
mkdir -p /config
if [ ! -f /config/yt-dlp.conf ]; then
    cp /app/default-yt-dlp.conf /config/yt-dlp.conf
fi

exec "$@"
