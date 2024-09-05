from dataclasses import dataclass

from .PlaylistEntry import PlaylistEntry


@dataclass
class Playlist:
    title: str
    filepath: str
    playlist_entries: dict[PlaylistEntry]
