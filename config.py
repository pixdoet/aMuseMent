"""
    config.py - Loads config options from config.json.
"""

import json
import os
import sys
from pathlib import Path


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def load_config():
    with open(resource_path("./config.json"), "r") as configFile:
        data = json.load(configFile)

    return data


# has to be here, cannot put into JSON
# when used must have leading slash!
# + new: add to user's home folder by default (can be and should be turned off asap)
fastFilePath = f"{Path.home()}/{load_config()['export_folder']}"
DEFAULT_SAVES_PATH = resource_path(os.path.abspath(fastFilePath))
