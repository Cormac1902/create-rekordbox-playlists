import os
import unittest

from playlist_creator import playlist_parser


class TestPlaylist(unittest.TestCase):
    def test_hash(self):
        test_title = 'Test Title'
        test_playlist = playlist_parser.Playlist(test_title)

        self.assertEqual({test_playlist}, {playlist_parser.Playlist(test_title)})

    def test_when_playlist_has_no_path_then_title_and_path_returns_title(self):
        test_title = 'Test Title'
        test_playlist = playlist_parser.Playlist(test_title)

        self.assertEqual(test_title, test_playlist.title_and_path)

    def test_when_playlist_has_path_then_title_and_path_returns_title_and_path(self):
        test_title = 'Test Title'
        test_path = '/test'
        test_playlist = playlist_parser.Playlist(
            test_title, path_from_playlists_directory=test_path
        )

        self.assertEqual(os.path.join(test_path, test_title), test_playlist.title_and_path)


if __name__ == '__main__':
    unittest.main()
