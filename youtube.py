from __future__ import unicode_literals
from yt_dlp import YoutubeDL

import os

def youtube_download(url):
    os.remove("youtube.wav")

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192'
        }],
        'postprocessor_args': [
            '-ar', '16000',
            '-ac', '1'
        ],
        'outtmpl': 'youtube.%(ext)s',
        # 'prefer_ffmpeg': True,
        'keepvideo': True
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return 'youtube.wav'

if __name__ == "__main__":
    youtube_download("https://www.youtube.com/watch?v=inpDLQLqSik")
