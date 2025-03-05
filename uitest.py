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

configData = config.load_config()
openInFinder = configData["itunes_options"]["add_to_itunes"]


# debug printing
def dprint(message):
    print(f"[UI_DBG_PRINT]: {message}")


# main app loop
def main(page: ft.Page):
    global configData, openInFinder, dprint

    def update_status(statusMessage):
        dprint(statusMessage)
        ui_statusMsg.value = statusMessage
        page.update()
        sleep(1)

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
                update_status("Unsupported playlist id!")
            else:
                download_phase_2(playlistData)

    def download_phase_2(playlistData):
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

    # os init
    def open_saves(e):
        osVersion = itunes.check_os_version()
        download.open_dir(osVersion=osVersion, savesPath=f"{config.DEFAULT_SAVES_PATH}")

    # change saves state
    def toggle_open_in_finder(e):
        global configData, openInFinder
        openInFinder = not openInFinder
        dprint(f"openInFinder now: {openInFinder}")
        ui_openInFinderItem.checked = openInFinder
        page.update()

    ui_openInFinderItem = ft.PopupMenuItem(
        text="Open after download?",
        checked=openInFinder,
        on_click=toggle_open_in_finder,
    )

    # init page
    page.title = "aMuseMent - the YouTube Music downloader"
    page.appbar = ft.AppBar(
        title=ft.Text("aMuseMent - the YouTube Music Downloader"),
        actions=[
            ft.PopupMenuButton(items=[ui_openInFinderItem]),
        ],
    )

    # draw layout
    ui_playlistId = ft.TextField(label="Enter playlist id")
    ui_statusMsg = ft.Text("Idle")
    page.add(
        ft.Row(
            [
                ui_playlistId,
            ]
        ),
        ft.Row(
            [
                ft.ElevatedButton("Download playlist!", on_click=download_playlist),
                ft.ElevatedButton(
                    "Open saves directory",
                    on_click=open_saves,
                ),
            ]
        ),
        ft.Row([ui_statusMsg]),
    )


ft.app(main)
