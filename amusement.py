#!/usr/bin/env python3

"""
aMuseMent - YTM to iTunes/AM conversion tool
Fully fledged with metadata!

(C) 2024 Ian Hiew - pixdo.et at gmail.com
"""

import sys

from amusement import amuse, arguments, cleaner, save_single, about


def main():
    args = arguments.parser.parse_args()
    if len(sys.argv) <= 1:
        amuse.main_download()

    # -c --clean_saves
    elif args.clean_saves:
        cleaner.wipe_all()
        exit()

    # -s --save_single
    elif args.save_single:
        print("Downloading in Single mode")
        songId = input("Enter song ID (no url): ")
        save_single.save_single_song(videoId=songId, uiMode=False)
        exit()

    # -ab --about
    elif args.about:
        about.print_about()
        exit()


if __name__ == "__main__":
    main()
