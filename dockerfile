# syntax=docker/dockerfile:1
FROM python:3.12.1-alpine3.18
WORKDIR /app
RUN apk update && \
    apk add --no-cache build-base ffmpeg && \
    rm -rf /var/cache/apk/*
COPY requirements.txt .
RUN python3 -m pip install --no-cache-dir -r requirements.txt

COPY youdis.py, default-yt-dlp.conf, update-ytdlp.sh run-youdis.sh /app/
RUN chmod +x /app/update-ytdlp.sh /app/run-youdis.sh

COPY weekly-restart /etc/cron.d/
RUN chmod 0644 /etc/cron.d/weekly-restart

ENTRYPOINT ["/app/run-youdis.sh"]
