from unittest.mock import MagicMock

from playlist_creator import playlist_parser, playlist_writer


#   pylint: disable=too-few-public-methods

class TestPlaylistWriterStrategy(playlist_writer.PlaylistWriterStrategy):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.write_playlist = MagicMock()

    def write_playlist(self,
                       playlist: playlist_parser.Playlist,
                       playlists_output_directory: str,
                       transcodes_output_directory: str):
        pass

#   pylint: enable=too-few-public-methods
