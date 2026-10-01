import requests

from amusement import config

configData = config.load_config()

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


def request_next(videoId: str):
    r = requests.post(
        url="https://music.youtube.com/youtubei/v1/next",
        headers={
            "accept": "application/json",
        },
        json={
            "context": YOUTUBEI_CONTEXT,
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
