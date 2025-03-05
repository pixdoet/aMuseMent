# aMuseMent
### A tool to download YouTube Music files and move them to iTunes/Apple Music

## Features
- 📁 Download directly from YouTube Music playlists at the highest quality possible!
- 📝 Music metadata prepared for you!
- 🎵 Add to iTunes automatically!

## Usage
1. **IMPORTANT!** Get `ffmpeg` for your relevant operating system and add it to your PATH:
    - https://www.ffmpeg.org/download.html
2. Download the binary from the Releases tab, right click and run!
3. Some configurations are on the menu on the top right corner. To edit all configurations, edit the file found when pressing "Open config.json folder" 

## Usage (command line)
1. Get `ffmpeg`, as above
2. Get Python 3.10 or newer
3. Clone / download repo to local system. Init venv (if needed)
4. Download requirements.txt: python3.10 -m pip install -r requirements.txt
5. Run `main.py` for the command line version or `amuse_ui.py` for the GUI version

## FAQ
Q: *Why am I stuck on downloading the first song?*

A: `ffmpeg` is not installed! Get it and make sure it's in your PATH.

Q: *Why no Windows add-to-iTunes?*

A: Add to iTunes on Windows is coming soon! I just need some time to figure out the correct directory for Windows iTunes.

Q: *Will this support Spotify?*

A: No. Spotify's API is too much of a hassle for me to deal with rn.

Q: *What is **FAST MODE**?*

A: 😏