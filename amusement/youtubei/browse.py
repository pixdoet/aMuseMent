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
            "context": YOUTUBEI_CONTEXT,
            "browseId": f"VL{browseId}",
        },
    )
    return r
