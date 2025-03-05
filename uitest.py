#!/usr/bin/env python3

"""
    uitest_flet: this time using flutter based!!!!!! excitement ensues
"""

import flet as ft
from time import sleep
import os

import arguments
import config
import cleaner
import download
import itunes
import playlist
import save_single
import tags
import youtubei

# globals
configData = config.load_config()


class Configures:
    def __init__(self):
        self.openInFinder = configData["download_options"][
            "open_in_finder_after_download"
        ]
        self.addToItunes = configData["itunes_options"]["add_to_itunes"]
        self.osVersion = itunes.check_os_version()
        self.fastMode = configData["ui_options"]["skip_status_update_wait_time"]
        self.updateWaitTime = configData["ui_options"]["status_update_wait_seconds"]


cfg = Configures()


# debug printing
def dprint(message):
    print(f"[UI_DBG_PRINT]: {message}")


# main app loop
def main(page: ft.Page):
    global configData, cfg, dprint

    # init page
    page.title = "aMuseMent - the YouTube Music downloader"
    # load font
    page.fonts = {
        "RobotoMono": "https://github.com/google/fonts/raw/refs/heads/main/apache/robotomono/RobotoMono%5Bwght%5D.ttf"
    }

    def update_status(statusMessage, wait: bool = True):
        dprint(statusMessage)
        ui_statusMsg.value = statusMessage
        page.update()
        if wait:
            if not cfg.fastMode:
                sleep(cfg.updateWaitTime)

    def download_playlist(e):
        if not ui_playlistId.value:
            ui_playlistId.error_text = "Enter playlist id"
            page.update()
        else:
            playlistInput = ui_playlistId.value
            update_status(f"Checking validity of {playlistInput}")

            # playlist checker
            playlistData = playlist.playlist_cleaner(playlistInput, uiMode=True)
            if not playlistData:
                update_status(
                    "Unsupported playlist id! Make sure you have pasted a valid playlist link"
                )
                ui_playlistId.error_text = "Unsupported playlist id!"
            else:
                download_phase_2(playlistData)

    def download_phase_2(playlistData):
        global configData, cfg, dprint
        playlistId = playlistData["id"]
        playlistType = playlistData["type"]
        update_status(f"Will download {playlistType} with id {playlistId}")

        # get browse resp n all songs
        browseResp = youtubei.request_browse(browseId=playlistId)
        parsedResp = youtubei.parse_youtubei(ytResponse=browseResp)

        # extract data
        for currentSong in parsedResp:
            # song metadata
            songId = currentSong["id"]
            songTitle = currentSong["title"]
            songArtist = currentSong["artist"]
            songAlbum = currentSong["album"]
            songThumbnailUrl = currentSong["thumbnail"]

            update_status(
                f"Now downloading: Video ID: {songId} | Title: {songTitle} | Author: {songArtist} | Album: {songAlbum}"
            )

            download.download_song(id=songId, playlistId=playlistId)
            update_status(f"Downloaded song: {songTitle}")

            tags.add_metadata(
                filePath=f"{config.DEFAULT_SAVES_PATH}/{playlistId}/{songId}.mp3",
                songTitle=songTitle,
                songArtist=songArtist,
                songAlbum=songAlbum,
                songThumbnailUrl=songThumbnailUrl,
            )

            update_status(f"Added metadata to song {songTitle}")

            os.rename(
                f"{config.DEFAULT_SAVES_PATH}/{playlistId}/{songId}.mp3",
                f"{config.DEFAULT_SAVES_PATH}/{playlistId}/{songTitle}.mp3",
            )

            update_status(f"Finished downloading song {songTitle}")

        update_status(f"Finished downloading playlist!")

        # add to itunes
        if cfg.addToItunes:
            update_status(f"Will add playlist to iTunes!")
            itunes.add_to_itunes(playlistId=playlistId, osVersion=cfg.osVersion)
            update_status(f"Finished adding to iTunes!")

        if cfg.openInFinder:
            download.open_dir(
                osVersion=cfg.osVersion,
                savesPath=f"{config.DEFAULT_SAVES_PATH}/{playlistId}",
            )

        update_status(f"Idle")

    # os init
    def open_saves(e):
        download.open_dir(
            osVersion=cfg.osVersion, savesPath=f"{config.DEFAULT_SAVES_PATH}"
        )

    # clear saves
    def clear_saves(e):
        update_status("ALL FILES from saves folder will be removed in 5 seconds")
        i = 0
        for i in range(5, 0, -1):
            update_status(f"Deleting in {i}...", wait=False)
            sleep(1)
        cleaner.wipe_all_fast()
        update_status("Done cleaning!")

    # appbar functions
    def toggle_open_in_finder(e):
        cfg.openInFinder = not cfg.openInFinder
        dprint(f"openInFinder now: {cfg.openInFinder}")
        ui_openInFinderItem.checked = cfg.openInFinder
        page.update()

    def toggle_add_to_itunes(e):
        cfg.addToItunes = not cfg.addToItunes
        dprint(f"addToItunes now: {cfg.addToItunes}")
        ui_addToItunesItem.checked = cfg.addToItunes
        page.update()

    def open_config_json(e):
        download.open_dir(osVersion=cfg.osVersion, savesPath=f"./config.json")

    def toggle_fast_mode(e):
        cfg.fastMode = not cfg.fastMode
        dprint(f"fastMode now: {cfg.fastMode}")
        ui_toggleFastMode.checked = cfg.fastMode
        page.update()

    ui_openInFinderItem = ft.PopupMenuItem(
        text="Open after download?",
        checked=cfg.openInFinder,
        on_click=toggle_open_in_finder,
    )
    ui_addToItunesItem = ft.PopupMenuItem(
        text="Add to iTunes?", checked=cfg.addToItunes, on_click=toggle_add_to_itunes
    )
    ui_openConfigJsonItem = ft.PopupMenuItem(
        text="Open config.json folder", on_click=open_config_json, icon="settings"
    )
    ui_toggleFastMode = ft.PopupMenuItem(
        text="FAST MODE", checked=cfg.fastMode, on_click=toggle_fast_mode
    )
    page.appbar = ft.AppBar(
        title=ft.Text(
            "aMuseMent - the YouTube Music Downloader",
            theme_style=ft.TextThemeStyle.HEADLINE_LARGE,
        ),
        actions=[
            ft.PopupMenuButton(
                items=[
                    ui_openInFinderItem,
                    ui_addToItunesItem,
                    ui_openConfigJsonItem,
                    ui_toggleFastMode,
                ]
            ),
        ],
    )

    # draw layout
    ui_playlistId = ft.TextField(label="Enter playlist id")
    ui_statusMsg = ft.Text("Idle", font_family="RobotoMono")
    page.add(
        ui_playlistId,
        ft.Row(
            [
                ft.ElevatedButton(
                    "Download playlist!", on_click=download_playlist, icon="download"
                ),
                ft.ElevatedButton(
                    "Open saves directory", on_click=open_saves, icon="folder"
                ),
            ]
        ),
        ft.ElevatedButton(
            "CLEAR SAVES DIRECTORY", on_click=clear_saves, icon="delete_rounded"
        ),
        ft.Divider(),
        ft.Text("Status: ", theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM),
        ft.Row([ui_statusMsg]),
    )


ft.app(main)
