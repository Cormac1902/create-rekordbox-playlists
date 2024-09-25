#   pylint: disable=too-few-public-methods

from abc import ABC, abstractmethod

from playlist_creator import playlist_parser


class PlaylistWriterStrategy(ABC):
    @abstractmethod
    def write_playlist(self,
                       playlist: playlist_parser.Playlist,
                       playlist_entries,
                       playlists_output_directory: str,
                       transcodes_output_directory: str):
        pass

#   pylint: enable=too-few-public-methods
