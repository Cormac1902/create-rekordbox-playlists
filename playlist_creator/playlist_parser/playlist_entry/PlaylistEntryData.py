from dataclasses import dataclass


@dataclass(frozen=True)
class PlaylistEntryData:
    file: str = None
    title: str = None
    length: str = None

    def __hash__(self):
        return hash(self.file)
