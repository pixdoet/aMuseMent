"""
playlist.py - seperated function for checking playlist types

TEST_URL: https://music.youtube.com/watch?v=826mxiKjoP0&list=RDAMVMgiMMVRK9hVU
"""


def playlist_or_video(playlistUrl: str):
    """
    playlist_or_video: what happens when u have video and playlist id in one url
    """
    while True:
        downloadMode = input(
            "Found a single song in a playlist URL. Download [p]laylist or [s]ong only? (p/s)"
        )

        if downloadMode == "p":
            print("Will download playlist")
            playlistUrlParse = playlistUrl.split("list=")
            playlistId = playlistUrlParse[1]
            print(f"Playlist ID: {playlistId}")
            return {"mode": "playlist", "id": playlistId}

        elif downloadMode == "s":
            print("Will download song")
            playlistUrlParse = playlistUrl.split("v=")
            videoId = playlistUrlParse[1][:11]
            print(f"Video ID: {videoId}")
            return {"mode": "single_video", "id": videoId}
        else:
            print("Please select playlist or song by typing p or s!")
            continue


def playlist_cleaner(playlistUrl: str, uiMode: bool):
    """
    playlist_cleaner: playlist url safety check!

    returns playlist id and playlist type

    playlist_types:
    playlist/album/radio playlist: normal playlist mode
    single_video: triggers single mode
    """

    # direct input playlist id
    if len(playlistUrl.split("list=")) <= 1:

        if "?v=" in playlistUrl:
            playlistInfo = {
                "type": "single_video",
                "id": playlistUrl.split("v=")[:11],
            }
            return playlistInfo

        else:
            if (
                len(playlistUrl) == 34
                or len(playlistUrl) == 36
                or len(playlistUrl) == 41
                or len(playlistUrl) == 43
            ):
                playlistId = playlistUrl

            # assume video id
            elif len(playlistUrl) == 11:
                playlistInfo = {"type": "single_video", "id": playlistUrl}
                return playlistInfo

            else:
                print("No valid playlist url/ID!")
                if not uiMode:
                    exit()
                else:
                    return False

    # check for ?v=
    if "v=" in playlistUrl:
        if "list=" in playlistUrl:
            # double url!
            downloadSelection = playlist_or_video(playlistUrl=playlistUrl)

            # found single video
            if downloadSelection["mode"] == "single_video":
                playlistInfo = {"type": "single_video", "id": downloadSelection["id"]}
                return playlistInfo
            elif downloadSelection["mode"] == "playlist":
                playlistId = downloadSelection["id"]

    # parse id from url
    else:
        playlistUrlParse = playlistUrl.split("list=")
        playlistId = playlistUrlParse[1]

    # start checking playlist id
    if playlistId.startswith("PL") or playlistId.startswith("VLPL"):
        if len(playlistId) == 34:
            playlistType = "playlist"
        if len(playlistId) == 36:
            playlistId = playlistId[2:]
            playlistType = "playlist"
        else:
            print("Wrong playlist id? Normal playlists need to have 34/36 characters")
            if not uiMode:
                exit()
            else:
                return False

    elif playlistId.startswith("OLAK"):
        if len(playlistId) == 41:
            playlistType = "album"
        else:
            print("Wrong album id? Normal albums need to have 41 characters")
            if not uiMode:
                exit()
            else:
                return False

    elif playlistId.startswith("RD"):
        if len(playlistId) == 43:
            playlistType = "radio playlist"
        else:
            print("Wrong radio id? Normal radios need to have 43 characters")
            if not uiMode:
                exit()
            else:
                return False
    else:
        print(
            "Wrong playlist ID or playlist currently not supported! Supports PL, OLAK and RD playlists only."
        )
        if not uiMode:
            exit()
        else:
            return False

    playlistInfo = {"id": playlistId, "type": playlistType}
    return playlistInfo
