from dataclasses import dataclass
from typing import Iterable

from playlist_creator import playlist_parser
from . import playlist_writer_strategy


@dataclass(frozen=True)
class PlaylistWriterContext:
    playlist: playlist_parser.Playlist
    playlists_output_directory: str
    transcodes_output_directory: str
    strategy: playlist_writer_strategy.PlaylistWriterStrategy
    _playlist_entries: Iterable[playlist_parser.PlaylistEntry]

    def write_playlist(self):
        self.strategy.write_playlist(
            self.playlist,
            self._playlist_entries,
            self.playlists_output_directory,
            self.transcodes_output_directory
        )
