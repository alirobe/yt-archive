# yt-archive

A lightweight Docker container for archiving YouTube channels using `yt-dlp`.

This repo is provided as-is, because it does what I want.

If you want to make customizations to this, fork it, adopt it, whatever, please go ahead. 

I am not interested in providing support or accepting pull requests, unless you are requesting to adopt the project. 

## Overview

You need to map `/data/`, and create a file called `channels.txt` in the root of it. This file contains newline delimited youtube channel names.

The container reads YouTube channel names and keep those channels mirrored locally in folders of the same name. 

It runs whenever it recieves a GET request to the path `/go` on its exposed port. This can be used for scheduling or testing. 

You can add this GET request to any task scheduler to ensure it happens regularly. yt-dlp does not re-download videos. For example powershell `curl "http://127.0.0.1:8205/go"` could be scheduled easily enough

## Prerequisites

- Docker
- A text file with the names of the YouTube channels to download, one per line.

## Building the Docker image

Build the Docker image with the following command:

```bash
docker build -t yt-archive .
```

## Running the Docker container

Run the Docker container with the following command:

```bash
docker run -d -v c:/youtube/:/data/ -p 8205:8205 --name yt-archive yt-archive
```

Replace `/path/on/host` with the path on your host machine where you will store the downloaded videos and where the `channels.txt` file is located. Replace `CRON_SCHEDULE` with your desired cron schedule in the format `minute hour day month day-of-week`.

## Saving the Docker image for import

Save the Docker image with the following command:

```bash
docker save yt-archive > yt-archive.tar
```

You can then `docker import` this `.tar` file, or upload it to your docker GUI (e.g. synology docker) as an image.

## Volumes

- `/data`: The path where the downloaded videos are stored and where the `channels.txt` file is located.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.