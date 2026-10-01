"""
parse.py - used to parse info from youtubei responses
"""

from amusement import config
from amusement.youtubei import youtubei, browse, next

configData = config.load_config()

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


def get_playlist_info(playlistId: str):
    """
    get_playlist_info: parse the youtubei info and return list of song metadata
    """
    browseResponse = browse.request_browse(browseId=playlistId)
    resp = browseResponse.json()

    playlistItems = []

    for i in resp["contents"]["twoColumnBrowseResultsRenderer"]["secondaryContents"][
        "sectionListRenderer"
    ]["contents"][0]["musicPlaylistShelfRenderer"]["contents"]:
        currentVidId = i["musicResponsiveListItemRenderer"]["playlistItemData"][
            "videoId"
        ]
        songInfoDict = get_song_info(
            videoId=currentVidId
        )  # use get_video_id from above (yeah)
        playlistItems.append(songInfoDict)

    return playlistItems
