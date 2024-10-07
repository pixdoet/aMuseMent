# aMuseMent `config.json` options

You've reached the uttermost uncomprehensible attrocity ever created by humanity!!!

## What?
This is the manual page for different configuration options. A `man` page for `config.json` if you will.

Starting now...

## `download_options`

Options for downloading files from YouTube and song metadata

---

### `placeholder_when_no_album` (bool)
Sets the album info even when there's no album info from YouTube.

`true`: A placeholder will be put as the album info

`false`: The album info will not be created

---

### `no_album_placeholder_text` (str)
Sets the album placeholder text if `placeholder_when_no_album` is `true`.

---

### `use_playlist_id_for_folder_name` (bool)
(CURRENTLY UNUSED) Uses the playlist id as the output folder's name. Affects **final output** only. Folder name will remain as playlist ID when download is under progress.

`true`: Uses playlist ID as folder name

`false`: Uses playlist title as folder name

---

### `download_postprocessor_options` (dict)
(CURRENTLY UNUSED) Postprocessor options for ffmpeg, used in `download.py`

---

## `itunes_options`

Options related to iTunes/AM library management.

### `add_to_itunes` (bool)
Determines if aMuseMent should add songs to iTunes/AM.

`true`: Adds songs to iTunes/AM.

`false`: Doesn't add songs to iTunes/AM. Downloaded mp3s sill available in `./saves/`

---

### `darwin` / `win32` / `cygwin`

"Add to iTunes/Apple Music" folder paths.

Depending on your OS, one of these will be used. Darwin = macOS, win32 = Windows (64 bit too!) and cygwin = python illiterates. These serve as platform identifiers for the following:

#### `iTunes_folder` (str) (darwin) (win32)
Folder for classic iTunes.

#### `am_folder` (str) (darwin) (win32?)
Apple music folder (with .localized)

#### `am_folder_alt` (str) (darwin) (win32?)
Apple music folder (no .localized)