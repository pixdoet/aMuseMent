"""
    config.py - loads config options from .json
"""

import json


def load_config():
    with open("config.json", "r") as configFile:
        data = json.load(configFile)

    return data
