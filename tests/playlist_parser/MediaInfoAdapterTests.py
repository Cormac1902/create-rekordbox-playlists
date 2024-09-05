import os
import unittest
from unittest.mock import PropertyMock, patch

from playlist_creator import playlist_parser


# noinspection PyUnusedLocal
class TestMediaInfoAdapter(unittest.TestCase):
    test_title = 'test'
    test_album_artist = 'test_album_artist'
    test_album = 'test_album'

    #   pylint: disable=unused-argument
    @patch.object(
        playlist_parser.MediaInfoAdapter,
        'disc',
        new_callable=PropertyMock(return_value=1)
    )
    def test_when_only_disc_has_value_then_formatted_filename_is_empty(self, disc):
        test_media_info_adapter = playlist_parser.MediaInfoAdapter()

        self.assertEqual(1, test_media_info_adapter.disc)
        self.assertEqual('', test_media_info_adapter.formatted_filename())

    @patch.object(
        playlist_parser.MediaInfoAdapter,
        'track',
        new_callable=PropertyMock(return_value=1)
    )
    def test_when_only_track_has_value_then_formatted_filename_returns_correctly(self, track):
        test_media_info_adapter = playlist_parser.MediaInfoAdapter()

        self.assertEqual('01', test_media_info_adapter.formatted_filename())

    @patch.object(
        playlist_parser.MediaInfoAdapter,
        'title',
        new_callable=PropertyMock(return_value=test_title)
    )
    def test_when_only_title_has_value_then_formatted_filename_returns_correctly(self, title):
        test_media_info_adapter = playlist_parser.MediaInfoAdapter()

        self.assertEqual(self.test_title, test_media_info_adapter.formatted_filename())

    @patch.object(
        playlist_parser.MediaInfoAdapter,
        'album_artist',
        new_callable=PropertyMock(return_value=test_album_artist)
    )
    def test_when_only_album_artist_has_value_then_formatted_filename_returns_correctly(
            self, album_artist
    ):
        test_media_info_adapter = playlist_parser.MediaInfoAdapter()

        self.assertEqual(self.test_album_artist, test_media_info_adapter.formatted_filename())

    @patch.object(
        playlist_parser.MediaInfoAdapter,
        'album',
        new_callable=PropertyMock(return_value=test_album)
    )
    def test_when_only_album_has_value_then_formatted_filename_returns_correctly(self, album):
        test_media_info_adapter = playlist_parser.MediaInfoAdapter()

        self.assertEqual(self.test_album, test_media_info_adapter.formatted_filename())

    @patch.object(
        playlist_parser.MediaInfoAdapter,
        'disc',
        new_callable=PropertyMock(return_value=1)
    )
    @patch.object(
        playlist_parser.MediaInfoAdapter,
        'track',
        new_callable=PropertyMock(return_value=1)
    )
    def test_when_only_disc_and_track_have_value_then_formatted_filename_returns_correctly(
            self, disc, track
    ):
        test_media_info_adapter = playlist_parser.MediaInfoAdapter()

        self.assertEqual('1-01', test_media_info_adapter.formatted_filename())

    @patch.object(
        playlist_parser.MediaInfoAdapter,
        'album',
        new_callable=PropertyMock(return_value=test_album)
    )
    @patch.object(
        playlist_parser.MediaInfoAdapter,
        'title',
        new_callable=PropertyMock(return_value=test_title)
    )
    def test_when_only_album_and_title_have_value_then_formatted_filename_returns_correctly(
            self, album, title
    ):
        test_media_info_adapter = playlist_parser.MediaInfoAdapter()

        self.assertEqual(
            os.sep.join([self.test_album, self.test_title]),
            test_media_info_adapter.formatted_filename()
        )

    @patch.object(
        playlist_parser.MediaInfoAdapter,
        'disc',
        new_callable=PropertyMock(return_value=1)
    )
    @patch.object(
        playlist_parser.MediaInfoAdapter,
        'track',
        new_callable=PropertyMock(return_value=1)
    )
    @patch.object(
        playlist_parser.MediaInfoAdapter,
        'album_artist',
        new_callable=PropertyMock(return_value=test_album_artist)
    )
    @patch.object(
        playlist_parser.MediaInfoAdapter,
        'album',
        new_callable=PropertyMock(return_value=test_album)
    )
    @patch.object(
        playlist_parser.MediaInfoAdapter,
        'title',
        new_callable=PropertyMock(return_value=test_title)
    )
#   pylint: disable=too-many-arguments
    def test_when_all_fields_have_value_then_formatted_filename_returns_correctly(
            self, disc, track, album_artist, album, title
    ):
        test_media_info_adapter = playlist_parser.MediaInfoAdapter()

        self.assertEqual(
            os.sep.join([self.test_album_artist, self.test_album, f"1-01 {self.test_title}"]),
            test_media_info_adapter.formatted_filename()
        )
#   pylint: enable=too-many-arguments


#   pylint: enable=unused-argument

if __name__ == '__main__':
    unittest.main()
