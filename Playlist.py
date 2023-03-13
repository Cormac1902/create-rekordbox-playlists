from typing import List

from PlaylistEntry import PlaylistEntry


class Playlist:
    playlist_entries: List[PlaylistEntry] = []

    def __init__(self, title, filepath):
        self.title: str = title
        self.filepath: str = filepath
