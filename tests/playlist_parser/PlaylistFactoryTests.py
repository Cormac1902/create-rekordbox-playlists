import os.path
import threading
import unittest
from unittest.mock import MagicMock

from playlist_creator import playlist_parser


class TestPlaylistFactory(unittest.TestCase):
    def test_lock_is_initialised(self):
        test_lock = threading.Lock()
        test_playlist_factory = playlist_parser.PlaylistFactory(test_lock)

        self.assertEqual(test_lock, test_playlist_factory._lock)

    def test_playlists_is_initialised(self):
        test_playlist_factory = playlist_parser.PlaylistFactory()

        self.assertEqual(set(), test_playlist_factory.playlists)

    def test_when_add_playlist_is_called_then_playlist_is_added(self):
        test_directory = '/test'
        test_file = 'Test.pls'
        test_playlist_factory = playlist_parser.PlaylistFactory()
        test_playlist_factory.add_playlist(test_directory, test_file)

        self.assertEqual(
            {playlist_parser.Playlist('Test', os.path.join(test_directory, test_file))},
            test_playlist_factory.playlists
        )

    def test_when_add_playlist_is_called_with_non_pls_file_then_playlist_is_not_added(self):
        test_directory = '/test'
        test_file = 'Test.m3u'
        test_playlist_factory = playlist_parser.PlaylistFactory()
        test_playlist_factory.add_playlist(test_directory, test_file)

        self.assertEqual(set(), test_playlist_factory.playlists)


if __name__ == '__main__':
    unittest.main()
