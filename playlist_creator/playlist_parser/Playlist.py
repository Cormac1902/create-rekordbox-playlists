from dataclasses import dataclass, field

from .PlaylistEntry import PlaylistEntry


@dataclass
class Playlist:
    title: str
    filepath: str
    playlist_entries: dict[PlaylistEntry] = field(default_factory=dict)
