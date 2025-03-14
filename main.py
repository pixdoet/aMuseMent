#!/usr/bin/env python3

"""
aMuseMent - YTM to iTunes/AM conversion tool
Fully fledged with metadata!

(C) 2024 Ian Hiew - pixdo.et at gmail.com
"""

# local imporT\
import about
import arguments
import config
import cleaner
import download
import itunes
import playlist
import save_single
import tags
import youtubei

# global imporT (taxed)
import os
import sys

configData = config.load_config()


# main download function / default mode
def main_download():
    # sanitize playlist url
    playlist_url = input("Enter playlist url/ID: ")

    playlistInfo = playlist.playlist_cleaner(playlistUrl=playlist_url, uiMode=False)

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
            filePath=f"{config.DEFAULT_SAVES_PATH}/{playlistId}/{songId}.mp3",
            songTitle=songTitle,
            songArtist=songArtist,
            songAlbum=songAlbum,
            songThumbnailUrl=songThumbnailUrl,
        )

        # safety check for if filename contains slash (/), replace with special char
        songFileName = songTitle.replace(
            "/", configData["download_options"]["replace_slash_with"]
        )
        # change filename to song title
        os.rename(
            f"{config.DEFAULT_SAVES_PATH}/{playlistId}/{songId}.mp3",
            f"{config.DEFAULT_SAVES_PATH}/{playlistId}/{songFileName}.mp3",
        )
        if songFileName != songTitle:
            print(f"Replaced character / with {configData['download_options']['replace_slash_with']}")
            print(f"New filename is {songFileName}")
        print(
            f"Change song name to {config.DEFAULT_SAVES_PATH}/{playlistId}/{songFileName}.mp3"
        )

    osVersion = itunes.check_os_version()

    # add to itunes
    if configData["itunes_options"]["add_to_itunes"]:

        if osVersion == "darwin" or osVersion == "win32" or osVersion == "cygwin":
            if osVersion == "darwin":
                itunes.add_to_itunes(playlistId=playlistId, osVersion="darwin")
            else:
                # windows moment
                None

        else:
            # y r u running dis on ur ms dos machine
            print("Device does not support iTunes/Apple Music! Exiting now...")
            exit()

    # open folder in Finder/explorer
    if configData["download_options"]["open_in_finder_after_download"]:
        download.open_dir(
            osVersion=osVersion, savesPath=f"{config.DEFAULT_SAVES_PATH}/{playlistId}"
        )
    print(f"Finished! Files can be found at {config.DEFAULT_SAVES_PATH}/{playlistId}")


def main():
    args = arguments.parser.parse_args()
    if len(sys.argv) <= 1:
        main_download()

    # -c --clean_saves
    elif args.clean_saves:
        cleaner.wipe_all()
        exit()

    # -s --save_single
    elif args.save_single:
        print("Downloading in Single mode")
        songId = input("Enter song ID (no url): ")
        save_single.save_single_song(songId)
        exit()

    # -ab --about
    elif args.about:
        about.print_about()
        exit()


if __name__ == "__main__":
    main()
