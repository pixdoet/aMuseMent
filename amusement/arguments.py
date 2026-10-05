import argparse

parser = argparse.ArgumentParser(description="aMuseMent - the YouTube Music downloader")

"""
-c / --clean_saves: clears files in save
"""
parser.add_argument(
    "-c", "--clean_saves", action="store_true", help="Cleans ./saves directory"
)
parser.add_argument(
    "-s", "--save_single", action="store_true", help="[Advanced] Save a single song"
)
parser.add_argument("-ab", "--about", action="store_true", help="About this tool")
