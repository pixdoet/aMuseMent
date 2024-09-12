# aMuseMent
### A tool to download YouTube Music files and move them to iTunes/AM

## Installation
1. Get python3.10 or newer
2. Clone / download repo to local system. Init venv (if needed)
3. Download requirements.txt: `python3.10 -m pip install -r requirements.txt`

## Usage
Run. `python3.10 main.py`

The script will ask you for a playlist URL / ID. Currently only supports playlist IDs starting with PL (normal playlists), this might change in the future.

Downloaded songs are saved in `./saves/{playlist id}/`. Song metadata and album art is already present.

## TODO
- Add to iTunes functionality for Windows / Mac
- CLI options
- Cleaner code