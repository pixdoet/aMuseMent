"""
thumbnails.py - Hosts functions regarding video thumbnails
"""


def thumbnail_treatment(thumbnailLink):
    """
    thumbnail_treatment: change thumbnail url to upscale to 1024p
    """
    if len(thumbnailLink.split("=")) != 2:
        return thumbnailLink
    else:
        oriThumbnail = thumbnailLink.split("=")[0]
        newThumb = f"{oriThumbnail}=w1024"
        return newThumb
