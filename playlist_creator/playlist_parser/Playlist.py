from dataclasses import dataclass, field


@dataclass(frozen=True)
class Playlist:
    title: str = None
    filepath: str = None
    playlist_entries: list = field(default_factory=list)

    def __hash__(self):
        return hash(self.title)
