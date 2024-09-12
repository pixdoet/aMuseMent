import eyed3
import urllib.request
import os


def add_metadata(filePath, songTitle, songArtist, songAlbum, songThumbnailUrl):
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


"""
add_metadata(
    "./test.mp3",
    "x",
    "y",
    "z",
    "https://lh3.googleusercontent.com/nAdmLnzWr-ZEV3bjzraE3YGFF36B2bhgUn7_AV9b4Ym_2Dy5xK2-aZxQVxFrQwuArQDeTdlFAlApr2M=w720",
)
"""
