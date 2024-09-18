import youtubei
import download
import tags

import os


def playlist_cleaner(playlistUrl: str):
    """
    playlist url safety check!

    if playlist doesn't split with list=, it's probably not something u like

    BUT there are specific IDs that we can use, PL, OLAK and RD

    """
    if len(playlistUrl.split("list=")) <= 1:
        if playlistUrl.startswith("PL"):
            if len(playlistUrl) == 34:
                playlistId = playlistUrl
                playlistType = "playlist"
            else:
                print("Wrong playlist id? Normal playlists need to have 34 characters")
                exit()

        elif playlistUrl.startswith("OLAK"):
            if len(playlistUrl) == 41:
                playlistId = playlistUrl
                playlistType = "album"
            else:
                print("Wrong album id? Normal albums need to have 41 characters")
                exit()

        elif playlistUrl.startswith("RD"):
            if len(playlistUrl) == 43:
                playlistId = playlistUrl
                playlistType = "radio playlist"
            else:
                print("Wrong radio id? Normal radios need to have 43 characters")
                exit()

        else:
            print("No valid playlist url/ID!")
            exit()
    else:
        playlistUrlParse = playlistId.split("list=")
        playlistId = playlistUrlParse[1]
        playlistType = "playlist link"

    playlistInfo = {"id": playlistId, "type": playlistType}
    return playlistInfo


def main():
    playlist_url = input("Enter playlist url: ")

    playlistInfo = playlist_cleaner(playlistUrl=playlist_url)

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
