"""
    config.py - Loads config options from config.json.
"""

import json
import os


def load_config():
    with open("config.json", "r") as configFile:
        data = json.load(configFile)

    return data


# has to be here, cannot put into JSON
# when used must have leading slash!
fastFilePath = load_config()["export_folder"]
DEFAULT_SAVES_PATH = os.path.abspath(fastFilePath)
