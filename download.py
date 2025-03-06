"""
    download.py - Wrapper function for yt_dlp to download videos
"""

import config

import os
import subprocess
import yt_dlp

import itunes  # for check_os_version

configData = config.load_config()
osVersion = itunes.check_os_version()


def download_song(id: str, playlistId: str):
    """
    download_song: downloads list of songs to folder, then saves to {config.DEFAULT_SAVES_PATH}/{playlistId}

    TODO - add download options to config.json
    """

    with yt_dlp.YoutubeDL(
        {
            "extract_audio": True,
            "format": "bestaudio/best",
            "outtmpl": f"{config.resource_path(config.DEFAULT_SAVES_PATH)}/{playlistId}/%(id)s",
            "ffmpeg_location": config.resource_path(
                configData["download_options"]["ffmpeg_path"][osVersion]
            ),
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
        return True


def open_dir(osVersion: str, savesPath: str):
    if osVersion == "win32":
        os.startfile(savesPath)
    elif osVersion == "darwin":
        subprocess.Popen(["open", savesPath])
    else:
        subprocess.Popen(["xdg-open", savesPath])
