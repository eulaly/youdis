# syntax=docker/dockerfile:1
FROM python:3.12.1-alpine3.18
WORKDIR /app
RUN apk update && \
    apk add --no-cache build-base ffmpeg && \
    rm -rf /var/cache/apk/*
COPY requirements.txt requirements.txt
RUN python3 -m pip install --no-cache-dir -r requirements.txt
COPY youdis.py youdis.py
COPY default-yt-dlp.conf /app/default-yt-dlp.conf
COPY create-ytdlp-config.sh /app/create-ytdlp-config.sh
RUN chmod 755 /app/create-ytdlp-config.sh
ENTRYPOINT ["/app/create-ytdlp-config.sh"]
CMD ["python3", "youdis.py"]