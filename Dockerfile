FROM python:3.10-slim-bullseye

LABEL maintainer="alirobe@alirobe.com" \
    version="1.0" \
    description="Docker image to archive YouTube channels using yt-dlp, runs whenever http://host:port/go recieves a GET request"

WORKDIR /app

COPY download_videos.sh /root/download_videos.sh
COPY server.py /app/server.py

RUN apt-get update && \
    apt-get install -y ffmpeg dos2unix && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir yt-dlp flask feedgen && \
    chmod +x /root/download_videos.sh

CMD ["python", "/app/server.py"]
