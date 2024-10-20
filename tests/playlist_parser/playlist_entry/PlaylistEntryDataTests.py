import unittest

from playlist_creator import playlist_parser


class TestPlaylistEntryData(unittest.TestCase):
    def test_hash(self):
        test_title = 'Test Title'
        test_playlist = playlist_parser.PlaylistEntryData(title=test_title)

        self.assertEqual({test_playlist}, {playlist_parser.PlaylistEntryData(title=test_title)})


if __name__ == '__main__':
    unittest.main()
