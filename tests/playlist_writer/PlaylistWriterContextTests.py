import unittest

from playlist_creator import playlist_parser, playlist_writer
from tests.playlist_writer.playlist_writer_strategy import TestPlaylistWriterStrategy


class TestPlaylistWriterContext(unittest.TestCase):
    def test_write_playlist_forwards_requests_to_strategy(self):
        test_playlist = playlist_parser.Playlist()
        test_playlist_writer_strategy = TestPlaylistWriterStrategy()
        test_playlist_writer_context = playlist_writer.PlaylistWriterContext(
            test_playlist, '', '', test_playlist_writer_strategy
        )

        test_playlist_writer_context.write_playlist()
        test_playlist_writer_strategy.write_playlist.assert_called_with(
            test_playlist, '', ''
        )


if __name__ == '__main__':
    unittest.main()
