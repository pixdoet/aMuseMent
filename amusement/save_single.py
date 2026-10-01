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
from amusement.youtubei import next, youtubei

configData = config.load_config()
osVersion = config.check_os_version()

PLACEHOLDER_WHEN_NO_ALBUM = configData["download_options"]["placeholder_when_no_album"]
NO_ALBUM_PLACEHOLDER_TEXT = configData["download_options"]["no_album_placeholder_text"]

CLIENT_VERSION = configData["download_options"]["youtubei_options"]["client_version"]
CLIENT_NAME = configData["download_options"]["youtubei_options"]["client_name"]


def get_song_info(videoId: str):
    nextData = next.request_next(videoId=videoId).json()

    ytmCheck = nextData["playerOverlays"]["playerOverlayRenderer"][
        "browserMediaSession"
    ]["browserMediaSessionRenderer"]

    songDetails = nextData["contents"]["singleColumnMusicWatchNextResultsRenderer"][
        "tabbedRenderer"
    ]["watchNextTabbedResultsRenderer"]["tabs"][0]["tabRenderer"]["content"][
        "musicQueueRenderer"
    ][
        "content"
    ][
        "playlistPanelRenderer"
    ][
        "contents"
    ][
        0
    ][
        "playlistPanelVideoRenderer"
    ]

    # check if ytm song
    if "album" in ytmCheck:
        isYtmSong = True
    else:
        # not song, stop getting album details
        isYtmSong = False
        if PLACEHOLDER_WHEN_NO_ALBUM:
            noAlbumText = NO_ALBUM_PLACEHOLDER_TEXT
        else:
            noAlbumText = ""

    finalSongInfo = {
        "id": videoId,
        "title": songDetails["title"]["runs"][0]["text"],
        "artist": songDetails["longBylineText"]["runs"][0]["text"],
        "thumbnail": youtubei.thumbnail_treatment(
            songDetails["thumbnail"]["thumbnails"][0]["url"]
        ),
        "isYtmSong": isYtmSong,
    }

    if isYtmSong:
        finalSongInfo["album"] = songDetails["longBylineText"]["runs"][2]["text"]
        finalSongInfo["releaseTime"] = songDetails["longBylineText"]["runs"][4]["text"]

    else:
        # use placeholders for non-song
        finalSongInfo["album"] = "unknown"
        finalSongInfo["releaseTime"] = noAlbumText

    return finalSongInfo


def save_single_song(videoId: str):
    # TODO: make ts a class
    currentSong = get_song_info(videoId=videoId)
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
            exit()

    if configData["download_options"]["open_in_finder_after_download"]:
        download.open_dir(
            osVersion=osVersion, savesPath=f"{config.DEFAULT_SAVES_PATH}/singles/"
        )

    print(f"Download finished! Song can be found in {finalSinglePath}")

    return True
