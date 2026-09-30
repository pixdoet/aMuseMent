"""
itunes.py - Add downloaded files to "Automatically add to iTunes" folder or smth
"""

import os
import sys
import pathlib
import shutil

from amusement import config

configData = config.load_config()
configData = configData["itunes_options"]  # DO NOT REMOVE: shortcut for this file
osVersion = config.check_os_version()

if osVersion == "darwin" or osVersion == "win32":
    homeDir = pathlib.Path.home()  # grab home directory

    # get am directory
    amFolder = f"{homeDir}{configData[osVersion]['am_folder']}"
    amAlt = f"{homeDir}{configData[osVersion]['am_folder_alt']}"
    itunesFolder = f"{homeDir}{configData[osVersion]['itunes_folder']}"


def use_am():
    """
    use_am: check for apple music usage (uses different dir)

    Doubles as safety check for if iTunes folder exists
    """
    if os.path.isdir(amFolder) or os.path.isdir(amAlt):
        print("Adding songs to Apple Music")
        return True
    elif os.path.isdir(itunesFolder):
        print("Adding songs to iTunes")
        return False
    else:
        print("No valid iTunes or Apple Music folder found!")
        print("Ensure these paths exist on your system: ")
        print(f"iTunes: {itunesFolder}")
        print(f"Apple Music: {amFolder} or {amAlt}")
        exit()


def add_to_itunes(playlistId: str, osVersion: str):
    """
    add_to_itunes: main function to copy local downloaded files to iTunes/AM Directory
    """
    # check AM usage
    useAm = use_am()
    if useAm:
        finalDir = amFolder
        musicService = "Apple Music"
    else:
        finalDir = itunesFolder
        musicService = "iTunes"

    localSaveDir = f"{config.DEFAULT_SAVES_PATH}/{playlistId}"
    print(f"Will copy folder {localSaveDir} to {finalDir}")

    # copy files
    # this should be the different part for osVersion
    if osVersion == "darwin":
        shutil.copytree(localSaveDir, finalDir, dirs_exist_ok=True)
    elif osVersion == "win32" or osVersion == "cygwin":
        shutil.copytree(localSaveDir, finalDir, dirs_exist_ok=True)

    print(f"Done! Open {musicService} and your songs should be there!")
    return 0


def add_single_itunes(singlePath: str, osVersion: str):
    useAm = use_am()
    if useAm:
        # get single from filename via singles folder
        finalDir = amFolder
        musicService = "Apple Music"
    else:
        finalDir = itunesFolder
        musicService = "iTunes"

    print(f"Operating in single mode - will copy {singlePath} to {finalDir} ")

    shutil.copy(singlePath, finalDir)

    print(f"Done! Open {musicService} and your songs should be there")
