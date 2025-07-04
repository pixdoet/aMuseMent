"""
save_single.py - youtubei.py, but for single video ids

Not used in playlist downloading due to redundancy and lag w/ multiple requests

Also: an all in one solution to downloading songs if you prefer, shld work alone w/ minimum requirements

Uses /next (wtf)
"""

import requests
import os
import time

import config
import download
import itunes
import tags

configData = config.load_config()

PLACEHOLDER_WHEN_NO_ALBUM = configData["download_options"]["placeholder_when_no_album"]
NO_ALBUM_PLACEHOLDER_TEXT = configData["download_options"]["no_album_placeholder_text"]

CLIENT_VERSION = configData["download_options"]["youtubei_options"]["client_version"]
CLIENT_NAME = configData["download_options"]["youtubei_options"]["client_name"]


def request_next(videoId: str):
    r = requests.post(
        url="https://music.youtube.com/youtubei/v1/next",
        headers={
            "accept": "application/json",
        },
        json={
            "context": {
                "client": {
                    "hl": "en",
                    "gl": "MY",
                    "visitorData": "CgtqSnJ2akN1WTlDcyixxYm3BjIKCgJNWRIEGgAgPw%3D%3D",
                    "userAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:130.0) Gecko/20100101 Firefox/130.0,gzip(gfe)",
                    "clientName": CLIENT_NAME,
                    "clientVersion": CLIENT_VERSION,
                    "originalUrl": "https://music.youtube.com/",
                },
                "user": {"lockedSafetyMode": True},
            },
            "isAudioOnly": True,
            "videoId": f"{videoId}",
            "index": 1,
            "watchEndpointMusicSupportedConfigs": {
                "hasPersistentPlaylistPanel": True,
                "musicVideoType": "MUSIC_VIDEO_TYPE_ATV",
            },
        },
    )
    return r


def thumbnail_treatment(thumbnailLink: str):
    """
    thumbnail_treatment: change thumbnail url to upscale to 1024p
    """
    if len(thumbnailLink.split("=")) != 2:
        return thumbnailLink
    else:
        oriThumbnail = thumbnailLink.split("=")[0]
        newThumb = f"{oriThumbnail}=w1024"
        return newThumb


def get_song_info(videoId: str):
    nextData = request_next(videoId=videoId).json()

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

    if isYtmSong:
        finalSongInfo = {
            "id": videoId,
            "title": songDetails["title"]["runs"][0]["text"],
            "artist": songDetails["longBylineText"]["runs"][0]["text"],
            "album": songDetails["longBylineText"]["runs"][2]["text"],
            "releaseTime": songDetails["longBylineText"]["runs"][4]["text"],
            "thumbnail": thumbnail_treatment(
                songDetails["thumbnail"]["thumbnails"][0]["url"]
            ),
            "isYtmSong": isYtmSong,
        }

    else:
        # use placeholders for non-song
        finalSongInfo = {
            "id": videoId,
            "title": songDetails["title"]["runs"][0]["text"],
            "artist": songDetails["longBylineText"]["runs"][0]["text"],
            "album": noAlbumText,
            "releaseTime": "unknown",
            "thumbnail": thumbnail_treatment(
                songDetails["thumbnail"]["thumbnails"][0]["url"]
            ),
            "isYtmSong": isYtmSong,
        }

    return finalSongInfo


def save_single_song(videoId: str, uiMode: bool):
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

    # rename song
    os.rename(
        f"{config.DEFAULT_SAVES_PATH}/singles/{videoId}.mp3",
        f"{config.DEFAULT_SAVES_PATH}/singles/{songTitle}.mp3",
    )
    print(f"Finished downloading song: {songTitle}!")

    # add to itunes
    osVersion = itunes.check_os_version()
    finalSinglePath = f"{config.DEFAULT_SAVES_PATH}/singles/{songTitle}.mp3"

    if configData["itunes_options"]["add_to_itunes"]:
        if osVersion == "darwin" or osVersion == "win32" or osVersion == "cygwin":
            if osVersion == "darwin":
                itunes.add_single_itunes(
                    singlePath=f"{finalSinglePath}",
                    osVersion="darwin",
                )
            else:
                print(f"Add to iTunes coming soon! Songs saved at {finalSinglePath}")
                if uiMode:
                    return {
                        "success": True,
                        "message": f"Successfully downloaded song {songTitle}! Add to iTunes is coming to your playform soon",
                    }
                else:
                    exit()

        else:
            print("Device does not support iTunes/Apple Music!")
            if uiMode:
                return {
                    "success": True,
                    "message": f"Successfully downloaded song {songTitle}! Add to iTunes is not available on your platform :(",
                }
            else:
                exit()

    if configData["download_options"]["open_in_finder_after_download"]:
        download.open_dir(
            osVersion=osVersion, savesPath=f"{config.DEFAULT_SAVES_PATH}/singles/"
        )

    print(f"Download finished! Song can be found in {finalSinglePath}")

    if uiMode:
        return {
            "success": True,
            "message": f"Successfully downloaded song {songTitle}!",
        }


# save_single_song(input("D: "))
