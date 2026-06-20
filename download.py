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

    download_options: dict = {
        "extract_audio": True,
        "format": "bestaudio",
        "outtmpl": f"{config.resource_path(config.DEFAULT_SAVES_PATH)}/{playlistId}/%(id)s",
        "no_cache_dir": True,
        "force_ipv4": True,
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

    # NEW: Use cookies
    if configData["download_options"]["cookie_options"]["use_cookies"]:
        print(
            "[ALERT]: A JS Runtime is required when using cookies! See https://github.com/yt-dlp/yt-dlp/wiki/EJS"
        )
        match configData["download_options"]["cookie_options"]["cookie_method"]:
            case "browser":
                download_options["cookiesfrombrowser"] = (
                    configData["download_options"]["cookie_options"][
                        "cookie_from_browser"
                    ],
                    None,
                    None,
                    None,
                )
            case "cookiefile":  # tba
                # download_options["cookiefile"] = configData["download_options"][
                #    "cookie_options"
                # ]["cookie_file"]
                print(
                    "Cookiefile support is coming soon. Please use browser cookies at the moment. Thanks!"
                )
            case _:
                raise ValueError

        # debug
        print(download_options)

    with yt_dlp.YoutubeDL() as video:
        video.download(id)
        return True


def open_dir(osVersion: str, savesPath: str):
    if osVersion == "win32":
        os.startfile(savesPath)
    elif osVersion == "darwin":
        subprocess.Popen(["open", savesPath])
    else:
        subprocess.Popen(["xdg-open", savesPath])
