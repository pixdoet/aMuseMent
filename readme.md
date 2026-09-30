# aMuseMent
### A tool to download YouTube Music files and move them to iTunes/Apple Music

## Features
- 📁 Download directly from YouTube Music playlists at the highest quality possible!
- 📝 Music metadata prepared for you!
- 🎵 Add to iTunes automatically!

## Usage (GUI)
> [!WARNING]
> The previous Flet-based GUI has been deprecated. Development efforts will focus on stablilizing the CLI version first.

## Usage (command line)
1. Get `ffmpeg` for your relevant operating system and add it to your PATH: https://www.ffmpeg.org/download.html
2. Get Python 3.14 or newer
3. Clone / download repo to local system. Init venv (if needed)
4. Download required libraries: `python3 -m pip install -r requirements.txt`
5. Run the program: `python3 amusement.py`


## FAQ

Q: *Will this support Spotify?*

A: No. Spotify's API is too much of a hassle for me to deal with rn.

Q: *Can the previous Flet-based GUI be used?*

A: You can use it if you know how to fix it, but no support/issues will be provided at this point...

Q: *When is the GUI version going to return?*

A: Hopefully within a month if I can stop procrastinating...?

## Building the app
If you for some inexplicable reason want to build this into a binary...
1. Get PyInstaller
2. Change the `binaries` section in `aMuseMent.spec` to point to your specific build of `ffmpeg`
    - _You probably don't need to do this unless you have an ultra special build of ffmpeg_
3. Run `pyinstaller aMuseMent.spec`