"""
    aMuseMent - YTM to iTunes/AM conversion tool
    Fully fledged with metadata!

    (C) 2024 Ian Hiew - pixdo.et at gmail.com
"""

# local imporT
import youtubei
import download
import tags
import playlist

import os


def main():
    playlist_url = input("Enter playlist url: ")

    playlistInfo = playlist.playlist_cleaner(playlistUrl=playlist_url)

    playlistId = playlistInfo["id"]
    playlistType = playlistInfo["type"]

    print(f"Downloading {playlistType} with id {playlistId}")

    # fetch songs
    browseResponse = youtubei.request_browse(browseId=playlistId)

    # parse & download
    print("List of songs: ")
    parsedResponse = youtubei.parse_youtubei(browseResponse)

    print("---------------------------------------")

    # individual song treatments
    for currentSong in parsedResponse:
        songId = currentSong["id"]

        # song metadata
        songTitle = currentSong["title"]
        songArtist = currentSong["artist"]
        songAlbum = currentSong["album"]
        songThumbnailUrl = currentSong["thumbnail"]
        print(
            f"Video ID: {songId} | Title: {songTitle} | Author: {songArtist} | Album: {songAlbum}"
        )

        # download
        download.download_song(id=songId, playlistId=playlistId)
        print(f"Downloaded song {songTitle}")

        # add song meta
        tags.add_metadata(
            filePath=f"./saves/{playlistId}/{songId}.mp3",
            songTitle=songTitle,
            songArtist=songArtist,
            songAlbum=songAlbum,
            songThumbnailUrl=songThumbnailUrl,
        )

        # change filename to song title
        os.rename(
            f"./saves/{playlistId}/{songId}.mp3",
            f"./saves/{playlistId}/{songTitle}.mp3",
        )

    print(f"Finished! Files can be found at ./saves/{playlistId}/")


if __name__ == "__main__":
    main()
