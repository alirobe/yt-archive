#!/bin/sh
set -e
dos2unix "/data/channels.txt"
while IFS= read -r LINE
do
  CHANNEL_NAME=$(echo "$LINE" | cut -d ',' -f 1)
  CHANNEL_URL=$(echo "$LINE" | cut -d ',' -f 2)
  FORMAT=$(echo "$LINE" | cut -d ',' -f 3)

  if [ -z "$CHANNEL_URL" ]; then
    CHANNEL_URL="https://www.youtube.com/@$CHANNEL_NAME"
  fi

  if [ -z "$FORMAT" ]; then
    FORMAT="bestvideo[height<=?1080]+bestaudio/best"
  fi

  mkdir -p "/data/${CHANNEL_NAME}"
  yt-dlp "$CHANNEL_URL" \
    --output "/data/${CHANNEL_NAME}/%(upload_date)s__%(id)s__%(title)s.%(ext)s" \
    --restrict-filenames \
    --download-archive "/data/${CHANNEL_NAME}/.download-archive" \
    --format "${FORMAT}" \
    --max-downloads 10  \
    | tee "/data/${CHANNEL_NAME}/download.log"
done < "/data/channels.txt"