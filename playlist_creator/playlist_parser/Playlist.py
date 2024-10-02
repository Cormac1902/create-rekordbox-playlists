import os

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Playlist:
    title: str = None
    filepath: str = None
    path_from_playlists_directory: str = None
    playlist_entries: list = field(default_factory=list)

    @property
    def title_and_path(self):
        if not self.path_from_playlists_directory:
            return self.title

        return os.path.join(self.path_from_playlists_directory, self.title)

    def __hash__(self):
        return hash(self.title_and_path)
