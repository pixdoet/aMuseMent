"""
save_single.py - youtubei.py, but for single video ids

Not used in playlist downloading due to redundancy and lag w/ multiple requests
Uses /next (wtf)
"""

import os
import time

from amusement import config
from amusement.download import download, tags
from amusement.itunes import itunes
from amusement.youtubei import parse

configData = config.load_config()
osVersion = config.check_os_version()


def save_single_song(videoId: str):
    # TODO: make ts a class
    currentSong = parse.get_song_info(videoId=videoId)
    songTitle = currentSong["title"]
    songArtist = currentSong["artist"]
    songAlbum = currentSong["album"]
    songThumbnailUrl = currentSong["thumbnail"]
    songReleaseTime = currentSong["releaseTime"]
    isYtm = currentSong["isYtmSong"]

    print("You are now in SINGLE-SAVING MODE.")
    time.sleep(3)
    print(
        f"Video ID: {videoId} | Is YouTube Music song: {isYtm} | Title: {songTitle} | Author: {songArtist} | Album: {songAlbum} | Year: {songReleaseTime} | Thumbnail: {songThumbnailUrl}"
    )

    download.download_song(id=videoId, playlistId="singles")

    downloadedFilePath = f"{config.DEFAULT_SAVES_PATH}/singles/{videoId}.mp3"

    # add metadata
    tags.add_metadata(
        filePath=downloadedFilePath,
        songTitle=songTitle,
        songArtist=songArtist,
        songAlbum=songAlbum,
        songThumbnailUrl=songThumbnailUrl,
    )

    # safety check for illegal chars
    if "/" in songTitle or "|" in songTitle or "\\" in songTitle:
        # songTitle = f"{videoId}"
        print(
            "Song title contains illegal filename characters (/, |, \\ etc.). Video ID used as song title."
        )
    else:
        # rename song
        os.rename(
            f"{config.DEFAULT_SAVES_PATH}/singles/{videoId}.mp3",
            f"{config.DEFAULT_SAVES_PATH}/singles/{songTitle}.mp3",
        )
    print(f"Finished downloading song: {songTitle}!")

    # add to itunes
    finalSinglePath = f"{config.DEFAULT_SAVES_PATH}/singles/{songTitle}.mp3"

    if configData["itunes_options"]["add_to_itunes"]:
        if osVersion == "darwin" or osVersion == "win32":
            itunes.add_single_itunes(
                singlePath=f"{finalSinglePath}",
                osVersion=osVersion,
            )

        else:
            print("Device does not support iTunes/Apple Music!")

    if configData["download_options"]["open_in_finder_after_download"]:
        download.open_dir(
            osVersion=osVersion,
            savesPath=f"{config.DEFAULT_SAVES_PATH}/singles/",
        )

    print(f"Download finished! Song can be found in {finalSinglePath}")

    return True
