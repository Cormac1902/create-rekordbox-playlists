from .PlaylistEntry import PlaylistEntry


class Playlist:
    def __init__(self, title, filepath):
        self.title: str = title
        self.filepath: str = filepath
        self.playlist_entries: dict[PlaylistEntry] = dict[PlaylistEntry]()
