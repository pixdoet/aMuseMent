"""
download.py - uses yt_dlp and ffmpeg to download/convert the video :)

REWRITTEN TO SUPPORT COOKIES WDYM YT IS BLOCKING DOWNLOADS?
"""

import os
import pathlib
import subprocess
import yt_dlp

import config

configData = config.load_config()


def download_song(id: str, playlistId: str):
    """
    download_song: downloads list of songs to folder, then saves to {config.DEFAULT_SAVES_PATH}/{playlistId}

    TODO - add download options to config.json
    """
    # debug print out loc
    print(
        f"DEBUG: {config.resource_path(config.DEFAULT_SAVES_PATH)}/{playlistId}/%(id)s"
    )
    download_options = {
        "extract_flat": "discard_in_playlist",
        "ffmpeg_location": "/Volumes/Internal/Code/python/aMuseMent/amuseLib/ffmpeg_darwin",
        "final_ext": "mp3",
        "format": "bestaudio/best",
        "fragment_retries": 10,
        "ignoreerrors": "only_download",
        "outtmpl": {"default": "%(id)s.%(ext)s"},
        "paths": {
            "home": f"{config.resource_path(config.DEFAULT_SAVES_PATH)}/{playlistId}"
        },
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "nopostoverwrites": False,
                "preferredcodec": "mp3",
                "preferredquality": "5",
            },
            {"key": "FFmpegConcat", "only_multi_video": True, "when": "playlist"},
        ],
        "retries": 10,
        "warn_when_outdated": True,
        "verbose": configData["download_options"]["ytdlp_verbose"],
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

    # make dir before download i think
    path = pathlib.Path(f"/Users/pixdoet/amusement/{playlistId}/")
    path.mkdir(parents=True, exist_ok=True)

    with yt_dlp.YoutubeDL(download_options) as video:
        video.download(f"https://www.youtube.com/watch?v={id}")
        return True


def open_dir(osVersion: str, savesPath: str):
    if osVersion == "win32":
        os.startfile(savesPath)
    elif osVersion == "darwin":
        subprocess.Popen(["open", savesPath])
    else:
        subprocess.Popen(["xdg-open", savesPath])
