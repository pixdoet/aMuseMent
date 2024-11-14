# aMuseMent
### A tool to download YouTube Music files and move them to iTunes/Apple Music


## Installation
1. Get Python 3.10 or newer
2. Clone / download repo to local system. Init venv (if needed)
3. Download requirements.txt: `python3.10 -m pip install -r requirements.txt`
4. Install `ffmpeg` (for song conversion, must install!!!): https://www.ffmpeg.org/download.html
    - Important! Make sure `ffmpeg` is in your PATH (especially Windows): [Windows](https://phoenixnap.com/kb/ffmpeg-windows) | [Mac](https://superuser.com/questions/624561/install-ffmpeg-on-os-x) | [Linux](https://en.wikipedia.org/wiki/Trollface#/media/File:Trollface.png)

## Usage
Run `python3.10 main.py`

The script will ask you for a playlist URL / ID. Currently only supports playlist IDs starting with PL(normal playlists), RD(radio) and OLAK(albums)

Downloaded songs are saved in `./saves/{playlist id}/`. Song metadata and album art is already present.

Songs are automatically added to iTunes/Apple Music, depending on which one you have. You can turn this behaviour off in `config.json`. Windows users will have songs saved to iTunes.

### HELLO: Linux users will not have iTunes functionality (no iTunes owo)

## TODO
(in order of importance)

- Add to iTunes (Windows)
- GUI
- CLI options
- Cleaner code