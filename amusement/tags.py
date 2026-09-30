"""
    tags.py - Tags the mp3 folders with info from YouTube Music
"""

import eyed3
import urllib.request
import os


def add_metadata(
    filePath: str,
    songTitle: str,
    songArtist: str,
    songAlbum: str,
    songThumbnailUrl: str,
):
    if os.path.isfile(filePath):
        currentSongFile = eyed3.load(filePath)
        thumbnailData = urllib.request.urlopen(songThumbnailUrl).read()

        currentSongFile.tag.title = songTitle
        currentSongFile.tag.artist = songArtist
        currentSongFile.tag.album = songAlbum
        currentSongFile.tag.images.set(3, thumbnailData, "image/jpeg", "Desc")

        currentSongFile.tag.save()
    else:
        print(f"No such file found on {filePath} !")
