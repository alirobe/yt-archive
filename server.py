from flask import Flask, request, Response, send_file
from feedgen.feed import FeedGenerator
from datetime import datetime, timezone

import os

import subprocess

app = Flask(__name__)

@app.route('/go', methods=['GET'])
def download():
    cmd = '/root/download_videos.sh'
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)

    def generate_output():
        for line in iter(process.stdout.readline, ''):
            yield line

    return Response(generate_output(), mimetype='text/plain')

@app.route('/feed/<path:foldername>', methods=['GET'])
def generate_rss_feed(foldername):
    # Prevent directory traversal attacks
    if '..' in foldername or foldername.startswith('/'):
        abort(400, 'Invalid foldername')

    videos_folder = os.path.join('/data', foldername)

    # Check if the videos folder exists
    if not os.path.isdir(videos_folder):
        abort(404, 'Videos folder does not exist')

    # Create a new RSS feed
    feed = FeedGenerator()
    feed.title(f'Downloaded Videos - {foldername}')
    feed.id(request.url_root[:-1] + request.path)
    feed.link(href=request.url_root[:-1] + request.path, rel='self')

    # Iterate over the video files in the folder and add entries to the feed
    for filename in os.listdir(videos_folder):
        if filename.endswith(('.mp4', '.mpeg', '.mkv', '.webm', '.avi', '.flv', '.mkv', '.mp3', '.vp9', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4v', '.3gp', '.ogv', '.asf', '.ts', '.aiff', '.alac', '.m4a', '.ac3', '.mp2', '.amr', '.mid', '.midi', '.opus', '.m4b', '.weba', '.wemb')):  # Update the file extensions as needed
            filepath = os.path.join(videos_folder, filename)

            # Extract metadata from the filename
            metadata = filename.split('__')  # Assuming the format: upload_date__video_id__video_title.ext
            upload_date = metadata[0].strip()
            video_id = metadata[1].strip()
            upload_datetime = datetime.strptime(upload_date, "%Y%m%d").replace(tzinfo=timezone.utc)
            video_title = metadata[2].strip()
            file_extension = os.path.splitext(filename)[1].strip('.')  # Extract the file extension dynamically

            entry = feed.add_entry()
            entry.id(request.url_root[:-1] + filepath)
            entry.title(video_title)
            entry.link(href=request.url_root[:-1] + f'/file/{foldername}/{filename}')  # Update the link to point to the file stream route
            entry.published(upload_datetime)
            entry.enclosure(url=request.url_root[:-1] + filepath, length=0, type=f'video/{file_extension}')  # Add the enclosure element with the file extension

    # Generate the RSS feed XML
    feed_xml = feed.atom_str(pretty=True)

    return feed_xml, 200, {'Content-Type': 'application/xml'}

@app.route('/file/<path:foldername>/<filename>', methods=['GET'])
def serve_file(foldername, filename):
    # Prevent directory traversal attacks
    if '..' in foldername or foldername.startswith('/'):
        abort(400, 'Invalid foldername')

    file_path = os.path.join('/data', foldername, filename)

    # Check if the file exists
    if not os.path.isfile(file_path):
        abort(404, 'File does not exist')

    # Stream the file to the client
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8781)
