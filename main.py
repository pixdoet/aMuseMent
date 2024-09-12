import youtubei
import download
import tags

import os


def main():
    playlist_url = input("Enter playlist url: ")

    """
    playlist url safety check!

    if playlist doesn't split with list=, it's probably not something u like
    BUT it might be a playlist id, if it starts with PL and has 34 chars
    """
    if len(playlist_url.split("list=")) <= 1:
        if playlist_url.startswith("PL"):
            if len(playlist_url) == 34:
                playlistId = playlist_url
            else:
                print(
                    "Wrong playlist id? Currently only supports normal playlists that start with PL"
                )
        else:
            print("Not valid playlist url/ID!")
            exit()
    else:
        playlistUrlParse = playlist_url.split("list=")
        playlistId = playlistUrlParse[1]

    print(f"Downloading: playlist id {playlistId}")

    # fetch songs
    browseResponse = youtubei.request_browse(browseId=playlistId)

    # parse & download
    print("List of songs: ")
    parsedResponse = youtubei.parse_youtubei(browseResponse)

    # individual treatments
    for currentSong in parsedResponse:
        songId = currentSong["id"]

        # song metadata
        songTitle = currentSong["title"]
        songArtist = currentSong["artist"]
        songAlbum = currentSong["album"]
        songThumbnailUrl = currentSong["thumbnail"]
        print(
            f"vID: {songId} | Title: {songTitle} | Author: {songArtist} | Album: {songAlbum}"
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
