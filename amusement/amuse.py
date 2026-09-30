### SAFETY CHECK ###
if __name__ == "__main__":
    print("""
The file for running aMuseMent has been moved to ../amusement.py.
Please update your configurations to reflect the new change.
""")
    exit()

# local imporT\
from amusement import config, download, itunes, playlist, save_single, tags, youtubei

# global imporT (taxed)
import os

configData = config.load_config()
osVersion = config.check_os_version()


# main download function / default mode
def main_download():
    # sanitize playlist url
    playlist_url = input("Enter playlist url/ID: ")

    playlistInfo = playlist.playlist_cleaner(playlistUrl=playlist_url)

    playlistId = playlistInfo["id"]
    playlistType = playlistInfo["type"]

    # check if single song mode
    if playlistType == "single_video":
        save_single.save_single_song(videoId=playlistId)
        exit()

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

        # safety check for if filename contains special chars (/, |), replace with usable char
        if "/" in songTitle or "|" in songTitle or "\\" in songTitle:
            print(
                "Song title contains illegal filename characters (/, |, \\ etc.). Video ID used as song title."
            )
        else:
            # change filename to song title
            os.rename(
                f"{config.DEFAULT_SAVES_PATH}/{playlistId}/{songId}.mp3",
                f"{config.DEFAULT_SAVES_PATH}/{playlistId}/{songTitle}.mp3",
            )
            print(
                f"Change song name to {config.DEFAULT_SAVES_PATH}/{playlistId}/{songTitle}.mp3"
            )

    # add to itunes
    if configData["itunes_options"]["add_to_itunes"]:
        if osVersion == "darwin" or osVersion == "win32" or osVersion == "cygwin":
            if osVersion == "darwin":
                itunes.add_to_itunes(playlistId=playlistId, osVersion="darwin")
            elif osVersion == "win32" or osVersion == "cygwin":
                # windows moment
                itunes.add_to_itunes(playlistId=playlistId, osVersion="win32")

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
