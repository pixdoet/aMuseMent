from nicegui import ui

import download
import platform
import yt_dlp


async def download_song(vidId: str):
    dialog.open()
    result.content = ""

    downloadStatus = download.download_song(
        id=vidId, playlistId="PLwkDqdjdOosGwmARW29PR9oyq-OsP25pa"
    )


with ui.dialog() as dialog, ui.card():
    result = ui.markdown()

ui.label("Video Downloader?????")
message = ui.input(label="Video ID?", value="Default id here...")
with ui.row().classes("download_buttons"):
    ui.button(text="Download!", on_click=lambda: download_song(vidId=message.value))
    ui.button(text="Download as mp4", on_click=print("Has download as mp4")).classes(
        "download_mp4"
    )

ui.run(reload=platform.system() != "Windows")
