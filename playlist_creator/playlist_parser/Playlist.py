from dataclasses import dataclass, field


@dataclass(frozen=True)
class Playlist:
    title: str
    filepath: str
    playlist_entries: set[str] = field(default_factory=set)

    def __hash__(self):
        return hash(self.title)
