"""
    download.py - Wrapper function for yt_dlp to download videos
"""

import yt_dlp


def download_song(id, playlistId):
    """
    download_song: downloads list of songs to folder

    TODO - add download options to config.json
    """
    with yt_dlp.YoutubeDL(
        {
            "extract_audio": True,
            "format": "bestaudio/best",
            "outtmpl": f"./saves/{playlistId}/%(id)s",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
        }
    ) as video:
        video.download(id)
