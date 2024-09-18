"""
    config.py - Loads config options from config.json.
"""

import json


def load_config():
    with open("config.json", "r") as configFile:
        data = json.load(configFile)

    return data
