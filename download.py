import yt_dlp


def download_song(id, playlistId):
    with yt_dlp.YoutubeDL(
        {
            "extract_audio": True,
            "format": "bestaudio/best",
            "outtmpl": f"./saves/{playlistId}/%(id)s",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
        }
    ) as video:
        video.download(id)


# download_song("DxpndDEAqGk")