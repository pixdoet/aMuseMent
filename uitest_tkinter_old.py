#!/usr/bin/env python3

import tkinter as tk
from time import sleep
import os
from threading import Thread

import arguments
import config
import cleaner
import download
import itunes
import playlist
import save_single
import tags
import youtubei

# import yt_dlp

# init tk window


class aMuseGUI(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        root.title("aMuseMent Downloader")

        self.titleLabel = tk.Label(text="aMusement - the YouTube Music Downloader")
        self.titleLabel.pack()

        self.playlistLabel = tk.Label(text="Enter playlist ID or URL:")
        self.playlistLabel.pack()

        self.playlistEntry = tk.Entry()
        self.playlistEntry.pack()

        self.downloadButton = tk.Button(
            text="Download", command=self.download_playlist_thread
        )
        self.downloadButton.pack()  # side="left")

        self.cleanButton = tk.Button(
            text="Clean saves dir", command=self.clean_saves_thread
        )
        self.cleanButton.pack()  # side="right")

        self.statusMsg = ""
        self.statusLabel = tk.Label(text=self.statusMsg)
        self.statusLabel.pack(side="bottom")

        self.statusIndicatorLabel = tk.Label(text="Current status:")
        self.statusIndicatorLabel.pack(side="bottom")

    def update_label(self, labelText: str, wait: bool = True):
        print(f"[UI]: {labelText}")
        self.statusLabel.configure(text=labelText)
        # must put to update label in loop
        root.update()

        # only unused with countdowns
        if wait:
            sleep(2)

    def download_playlist(self):
        # get playlist ID
        self.playlistInput = self.playlistEntry.get()

        # run through playlist checker
        self.playlistData = playlist.playlist_cleaner(self.playlistInput)
        self.playlistId = self.playlistData["id"]
        self.playlistType = self.playlistData["type"]
        print(self.playlistId)

        self.update_label(
            labelText=f"Will download {self.playlistType}: {self.playlistId}",
        )

        # start download
        self.browseResponse = youtubei.request_browse(browseId=self.playlistId)

        # get all songs
        self.parsedResponse = youtubei.parse_youtubei(ytResponse=self.browseResponse)

        for currentSong in self.parsedResponse:
            self.songId = currentSong["id"]

            # song metadata
            self.songTitle = currentSong["title"]
            self.songArtist = currentSong["artist"]
            self.songAlbum = currentSong["album"]
            self.songThumbnailUrl = currentSong["thumbnail"]

            self.update_label(
                f"Video ID: {self.songId} | Title: {self.songTitle} | Author: {self.songArtist} | Album: {self.songAlbum}"
            )

            # download
            download.download_song(id=self.songId, playlistId=self.playlistId)
            self.update_label(f"Downloaded song {self.songTitle}")

            # add song meta
            tags.add_metadata(
                filePath=f"{config.DEFAULT_SAVES_PATH}/{self.playlistId}/{self.songId}.mp3",
                songTitle=self.songTitle,
                songArtist=self.songArtist,
                songAlbum=self.songAlbum,
                songThumbnailUrl=self.songThumbnailUrl,
            )

            # change filename to song title
            os.rename(
                f"{config.DEFAULT_SAVES_PATH}/{self.playlistId}/{self.songId}.mp3",
                f"{config.DEFAULT_SAVES_PATH}/{self.playlistId}/{self.songTitle}.mp3",
            )
            self.update_label(
                f"Change song name to {config.DEFAULT_SAVES_PATH}/{self.playlistId}/{self.songTitle}.mp3"
            )

        self.update_label(f"Finished downloading playlist!")

        osVersion = itunes.check_os_version()
        self.openFinderButton = tk.Button(
            text="Open download location",
            command=download.open_dir(
                osVersion=osVersion,
                savesPath=f"{config.DEFAULT_SAVES_PATH}/{self.playlistId}",
            ),
        )
        self.openFinderButton.pack(side="bottom")
        root.update()

    def clean_saves(self):
        self.update_label("ALL FILES from saves folder will be removed in 5 seconds")
        i = 0
        for i in range(5, 0, -1):
            self.update_label(f"Deleting in {i}...", wait=False)
            sleep(1)
        cleaner.wipe_all_fast()
        self.update_label("Done cleaning!")

    # wish there was some more elegant way of doing this
    def download_playlist_thread(self):
        t = Thread(target=self.download_playlist, args=(), daemon=True)
        t.run()

    def clean_saves_thread(self):
        t = Thread(target=self.clean_saves, args=(), daemon=True)
        t.run()


if __name__ == "__main__":
    root = tk.Tk()
    gui = aMuseGUI(root)
    gui.mainloop()
