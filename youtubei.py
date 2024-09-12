import requests
import os


def request_browse(browseId: str):
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
                    "remoteHost": "180.74.65.60",
                    "deviceMake": "Apple",
                    "deviceModel": "",
                    "visitorData": "CgtqSnJ2akN1WTlDcyixxYm3BjIKCgJNWRIEGgAgPw%3D%3D",
                    "userAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:130.0) Gecko/20100101 Firefox/130.0,gzip(gfe)",
                    "clientName": "WEB_REMIX",
                    "clientVersion": "1.20240909.01.00",
                    "osName": "Macintosh",
                    "osVersion": "10.15",
                    "originalUrl": "https://music.youtube.com/",
                    "timeZone": "Asia/Kuala_Lumpur",
                    "browserName": "Firefox",
                    "browserVersion": "130.0",
                    "acceptHeader": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/png,image/svg+xml,*/*;q=0.8",
                    "deviceExperimentId": "ChxOelF4TXpVNU5qUTFNRE0wTlRFd01qYzRNQT09ELHFibcGGLHFibcG",
                    "musicAppInfo": {
                        "pwaInstallabilityStatus": "PWA_INSTALLABILITY_STATUS_UNKNOWN",
                        "webDisplayMode": "WEB_DISPLAY_MODE_BROWSER",
                        "storeDigitalGoodsApiSupportStatus": {
                            "playStoreDigitalGoodsApiSupportStatus": "DIGITAL_GOODS_API_SUPPORT_STATUS_UNSUPPORTED"
                        },
                    },
                },
                "user": {"lockedSafetyMode": False},
                "request": {
                    "useSsl": True,
                    "internalExperimentFlags": [],
                    "consistencyTokenJars": [],
                },
            },
            "browseId": f"VL{browseId}",
        },
    )
    return r


def thumbnail_treatment(thumbnailLink):
    """
    treatment for thumbnails to upscale to 1024p or smth
    """
    if len(thumbnailLink.split("=")) != 2:
        return thumbnailLink
    else:
        oriThumbnail = thumbnailLink.split("=")[0]
        newThumb = f"{oriThumbnail}=w1024"
        return newThumb


# PLmWlbzfaYIsSFQRQtKAGKWg4xv-CYhqLM
def parse_youtubei(ytResponse):
    """
    parse the youtubei info and return list of song metadata
    """
    resp = ytResponse.json()

    playlistItems = []

    for i in resp["contents"]["twoColumnBrowseResultsRenderer"]["secondaryContents"][
        "sectionListRenderer"
    ]["contents"][0]["musicPlaylistShelfRenderer"]["contents"]:
        currentVidId = i["musicResponsiveListItemRenderer"]["playlistItemData"][
            "videoId"
        ]
        # print(currentVidId)

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

        # check if song name exist, if not use vid info
        if len(songAlbumAccessor) <= 0:
            # not a song!
            currentSongTitle = songTitleAccessor["runs"][0]["text"]
            currentSongAuthor = songAuthorAccessor["runs"][0]["text"]
            currentSongAlbum = "unknown - not a song!"

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

        # print data
        print(
            f"vID: {currentVidId} | Title: {currentSongTitle} | Author: {currentSongAuthor} | Album: {currentSongAlbum}"
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


# testing!
# tc = parse_youtubei(request_browse(browseId="PLwkDqdjdOosFYPXv-v3n861GnmOImt1Ki"))
# for a in tc:
#    print(a["songInfo"]["thumbnail"])
