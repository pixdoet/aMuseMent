"""
playlist.py - seperated function for checking playlist types
"""


def playlist_cleaner(playlistUrl: str, uiMode: bool):
    """
    playlist_cleaner: playlist url safety check!

    returns playlist id and playlist type
    """

    # direct input playlist id
    if len(playlistUrl.split("list=")) <= 1:
        if (
            len(playlistUrl) == 34
            or len(playlistUrl) == 36
            or len(playlistUrl) == 41
            or len(playlistUrl) == 43
        ):
            playlistId = playlistUrl
        else:
            print("No valid playlist url/ID!")
            if not uiMode:
                exit()
            else:
                return False
    # parse id from url
    else:
        playlistUrlParse = playlistUrl.split("list=")
        playlistId = playlistUrlParse[1]

    # start checking playlist id
    if playlistId.startswith("PL") or playlistId.startswith("VLPL"):
        if len(playlistId) == 34 or len(playlistId) == 36:
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
