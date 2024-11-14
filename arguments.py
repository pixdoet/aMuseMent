import argparse

parser = argparse.ArgumentParser(description="aMuseMent - the YouTube Music downloader")

"""
-c / --clean_saves: clears files in save
"""
parser.add_argument(
    "-c", "--clean_saves", action="store_true", help="Cleans ./saves directory"
)
