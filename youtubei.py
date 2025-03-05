"""
    youtubei.py - requests youtubei for music info
"""

import requests
import config

configData = config.load_config()

PLACEHOLDER_WHEN_NO_ALBUM = configData["download_options"]["placeholder_when_no_album"]
NO_ALBUM_PLACEHOLDER_TEXT = configData["download_options"]["no_album_placeholder_text"]

CLIENT_VERSION = configData["download_options"]["youtubei_options"]["client_version"]
CLIENT_NAME = configData["download_options"]["youtubei_options"]["client_name"]


def request_browse(browseId: str):
    """
    request_browse: requests youtubei browse for raw data
    """
    r = requests.post(
        url="https://music.youtube.com/youtubei/v1/browse",
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
            },
            "browseId": f"VL{browseId}",
        },
    )
    return r


def thumbnail_treatment(thumbnailLink):
    """
    thumbnail_treatment: change thumbnail url to upscale to 1024p
    """
    if len(thumbnailLink.split("=")) != 2:
        return thumbnailLink
    else:
        oriThumbnail = thumbnailLink.split("=")[0]
        newThumb = f"{oriThumbnail}=w1024"
        return newThumb


def parse_youtubei(ytResponse):
    """
    parse_youtubei: parse the youtubei info and return list of song metadata
    """
    resp = ytResponse.json()

    playlistItems = []

    for i in resp["contents"]["twoColumnBrowseResultsRenderer"]["secondaryContents"][
        "sectionListRenderer"
    ]["contents"][0]["musicPlaylistShelfRenderer"]["contents"]:
        currentVidId = i["musicResponsiveListItemRenderer"]["playlistItemData"][
            "videoId"
        ]
        # start getting info
        songTitleAccessor = i["musicResponsiveListItemRenderer"]["flexColumns"][0][
            "musicResponsiveListItemFlexColumnRenderer"
        ]["text"]
        songAuthorAccessor = i["musicResponsiveListItemRenderer"]["flexColumns"][1][
            "musicResponsiveListItemFlexColumnRenderer"
        ]["text"]
        songAlbumAccessor = i["musicResponsiveListItemRenderer"]["flexColumns"][2][
            "musicResponsiveListItemFlexColumnRenderer"
        ]["text"]

        # check if song album exist, if not use vid info
        if len(songAlbumAccessor) <= 0:
            # not a song!
            currentSongTitle = songTitleAccessor["runs"][0]["text"]
            currentSongAuthor = songAuthorAccessor["runs"][0]["text"]
            if PLACEHOLDER_WHEN_NO_ALBUM:
                currentSongAlbum = NO_ALBUM_PLACEHOLDER_TEXT
            else:
                currentSongAlbum = ""

        else:
            # is a song
            currentSongTitle = songTitleAccessor["runs"][0]["text"]
            currentSongAuthor = songAuthorAccessor["runs"][0]["text"]
            currentSongAlbum = songAlbumAccessor["runs"][0]["text"]

        currentThumbnail = thumbnail_treatment(
            i["musicResponsiveListItemRenderer"]["thumbnail"]["musicThumbnailRenderer"][
                "thumbnail"
            ]["thumbnails"][0]["url"]
        )

        # print data (redundant?)
        print(
            f"Video ID: {currentVidId} | Title: {currentSongTitle} | Author: {currentSongAuthor} | Album: {currentSongAlbum}"
        )

        songInfoDict = {
            "id": currentVidId,
            "title": currentSongTitle,
            "artist": currentSongAuthor,
            "album": currentSongAlbum,
            "thumbnail": currentThumbnail,
            "isYtmSong": True,
        }
        playlistItems.append(songInfoDict)

    return playlistItems
