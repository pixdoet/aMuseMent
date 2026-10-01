"""
youtubei.py - requests youtubei for music info
"""

from amusement import config

configData = config.load_config()

PLACEHOLDER_WHEN_NO_ALBUM = configData["download_options"]["placeholder_when_no_album"]
NO_ALBUM_PLACEHOLDER_TEXT = configData["download_options"]["no_album_placeholder_text"]

CLIENT_VERSION = configData["download_options"]["youtubei_options"]["client_version"]
CLIENT_NAME = configData["download_options"]["youtubei_options"]["client_name"]

YOUTUBEI_CONTEXT = {
    "client": {
        "hl": "en",
        "gl": "MY",
        "visitorData": "CgtqSnJ2akN1WTlDcyixxYm3BjIKCgJNWRIEGgAgPw%3D%3D",
        "userAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:130.0) Gecko/20100101 Firefox/130.0,gzip(gfe)",
        "clientName": CLIENT_NAME,
        "clientVersion": CLIENT_VERSION,
        "originalUrl": "https://music.youtube.com/",
    },
}


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
