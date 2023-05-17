# yt-archive

A lightweight Docker container for archiving personal YouTube channels using `yt-dlp`.

This repo is provided as-is, because it does what I want. It contains minimal code, so it should be trustable. (The serve_file and generate_rss_feed functions can be removed if not needed)

If you want it to do what you want, go ahead and fork it, adopt it, whatever. I don't care, but I also can't guarantee I'll be around to give support or accept pull requests.

## Setting this up

The container reads YouTube channel list and keep those channels mirrored locally in folders of the same name. 

It runs whenever it recieves a GET request to the path `/go` on its exposed port. This can be used for scheduling or testing. 

You can add this GET request to any task scheduler to ensure it happens regularly. yt-dlp does not re-download videos. For example bash/powershell `curl "http://127.0.0.1:8781/go"` could be scheduled easily enough, and you can also run this in the browser if you want a manual approach.

Please note that to avoid throttling this won't download more than 10 videos per channel per execution. You could just run it every day until the archive is filled, as already downloaded videos don't count towards the quota.

The archive also provides an RSS feed of the folders it controls. 

## Setup

- You need Docker
- A folder mapped to `/data/`
- A text file with the names of the YouTube channels to download, formatted as per `channels.txt.sample`, in the root.

## Building the Docker image

Build the Docker image with the following command:

```bash
docker build -t yt-archive .
```

## Running the Docker container

Run the Docker container with the following command:

```bash
docker run -d -v c:/youtube/:/data/ -p 8781:8781 --name yt-archive yt-archive
```

Replace `c:/youtube/` with the path on your host machine where you will store the downloaded videos; and where the `channels.txt` file is located.

## Saving the Docker image for import

If you're running this on a NAS device, you'll want to save the Docker image with the following command:

```bash
docker save yt-archive > yt-archive.tar
```

You can then copy the tar file to your target, and either run `docker import` on the `.tar` file, or upload it to your docker GUI as an image.

## Volumes

- `/data`: The path where the downloaded videos are stored and where the `channels.txt` file is located.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.