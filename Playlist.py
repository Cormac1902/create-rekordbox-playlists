from PlaylistEntry import PlaylistEntry


class Playlist:
    playlist_entries: dict[PlaylistEntry]

    def __init__(self, title, filepath):
        self.title: str = title
        self.filepath: str = filepath
        self.playlist_entries = dict()
