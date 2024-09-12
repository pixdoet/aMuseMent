# aMuseMent
### A tool to download YouTube Music files and move them to iTunes/AM

## IMPORTANT: Linux users will not have iTunes functionality (duh, no iTunes)

## Installation
1. Get python3.10 or newer
2. Clone / download repo to local system. Init venv (if needed)
3. Download requirements.txt: `python3.10 -m pip install -r requirements.txt`
4. Install `ffmpeg` (for song conversion, must install!!!): https://www.ffmpeg.org/download.html
    - Important! Make sure `ffmpeg` is in your PATH (especially Windows): [Windows](https://phoenixnap.com/kb/ffmpeg-windows) | [Mac](https://superuser.com/questions/624561/install-ffmpeg-on-os-x) | [Linux](https://en.wikipedia.org/wiki/Trollface#/media/File:Trollface.png)

## Usage
Run. `python3.10 main.py`

The script will ask you for a playlist URL / ID. Currently only supports playlist IDs starting with PL (normal playlists), this might change in the future.

Downloaded songs are saved in `./saves/{playlist id}/`. Song metadata and album art is already present.

## TODO
- Add to iTunes functionality for Windows / Mac
- CLI options
- Cleaner code