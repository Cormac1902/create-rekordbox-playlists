import os
import unittest
from unittest.mock import MagicMock, PropertyMock, patch

from playlist_creator import playlist_parser


# noinspection PyUnusedLocal
class TestMetadataAdapter(unittest.TestCase):
    test_title = 'test'
    test_album_artist = 'test_album_artist'
    test_album = 'test_album'

    def test_get_tag(self):
        test_tag = 'test_tag'
        test_value = 'Test'
        test_tags = { test_tag: test_value }

        self.assertEqual(playlist_parser.get_tag(test_tags, test_tag), test_value)

    #   pylint: disable=unused-argument
    @patch.object(
        playlist_parser.MetadataAdapter,
        'disc',
        new_callable=PropertyMock(return_value=1)
    )
    def test_when_only_disc_has_value_then_formatted_filename_is_empty(self, disc):
        test_metadata_adapter = playlist_parser.MetadataAdapter()

        self.assertEqual(1, test_metadata_adapter.disc)
        self.assertEqual('', test_metadata_adapter.formatted_filename())

    @patch.object(
        playlist_parser.MetadataAdapter,
        'track',
        new_callable=PropertyMock(return_value=1)
    )
    def test_when_only_track_has_value_then_formatted_filename_returns_correctly(self, track):
        test_metadata_adapter = playlist_parser.MetadataAdapter()

        self.assertEqual('01', test_metadata_adapter.formatted_filename())

    @patch.object(
        playlist_parser.MetadataAdapter,
        'title',
        new_callable=PropertyMock(return_value=test_title)
    )
    def test_when_only_title_has_value_then_formatted_filename_returns_correctly(self, title):
        test_metadata_adapter = playlist_parser.MetadataAdapter()

        self.assertEqual(self.test_title, test_metadata_adapter.formatted_filename())

    @patch.object(
        playlist_parser.MetadataAdapter,
        'album_artist',
        new_callable=PropertyMock(return_value=test_album_artist)
    )
    def test_when_only_album_artist_has_value_then_formatted_filename_returns_correctly(
            self, album_artist
    ):
        test_metadata_adapter = playlist_parser.MetadataAdapter()

        self.assertEqual(self.test_album_artist, test_metadata_adapter.formatted_filename())

    @patch.object(
        playlist_parser.MetadataAdapter,
        'album',
        new_callable=PropertyMock(return_value=test_album)
    )
    def test_when_only_album_has_value_then_formatted_filename_returns_correctly(self, album):
        test_metadata_adapter = playlist_parser.MetadataAdapter()

        self.assertEqual(self.test_album, test_metadata_adapter.formatted_filename())

    @patch.object(
        playlist_parser.MetadataAdapter,
        'disc',
        new_callable=PropertyMock(return_value=1)
    )
    @patch.object(
        playlist_parser.MetadataAdapter,
        'track',
        new_callable=PropertyMock(return_value=1)
    )
    def test_when_only_disc_and_track_have_value_then_formatted_filename_returns_correctly(
            self, disc, track
    ):
        test_metadata_adapter = playlist_parser.MetadataAdapter()

        self.assertEqual('1-01', test_metadata_adapter.formatted_filename())

    @patch.object(
        playlist_parser.MetadataAdapter,
        'album',
        new_callable=PropertyMock(return_value=test_album)
    )
    @patch.object(
        playlist_parser.MetadataAdapter,
        'title',
        new_callable=PropertyMock(return_value=test_title)
    )
    def test_when_only_album_and_title_have_value_then_formatted_filename_returns_correctly(
            self, album, title
    ):
        test_metadata_adapter = playlist_parser.MetadataAdapter()

        self.assertEqual(
            os.sep.join([self.test_album, self.test_title]),
            test_metadata_adapter.formatted_filename()
        )

    @patch.object(
        playlist_parser.MetadataAdapter,
        'disc',
        new_callable=PropertyMock(return_value=1)
    )
    @patch.object(
        playlist_parser.MetadataAdapter,
        'track',
        new_callable=PropertyMock(return_value=1)
    )
    @patch.object(
        playlist_parser.MetadataAdapter,
        'album_artist',
        new_callable=PropertyMock(return_value=test_album_artist)
    )
    @patch.object(
        playlist_parser.MetadataAdapter,
        'album',
        new_callable=PropertyMock(return_value=test_album)
    )
    @patch.object(
        playlist_parser.MetadataAdapter,
        'title',
        new_callable=PropertyMock(return_value=test_title)
    )
#   pylint: disable=too-many-arguments
    def test_when_all_fields_have_value_then_formatted_filename_returns_correctly(
            self, disc, track, album_artist, album, title
    ):
        test_metadata_adapter = playlist_parser.MetadataAdapter()

        self.assertEqual(
            os.sep.join([self.test_album_artist, self.test_album, f"1-01 {self.test_title}"]),
            test_metadata_adapter.formatted_filename()
        )
#   pylint: enable=too-many-arguments
    def test_get_returns_from_metadata(self):
        test_metadata_adapter = playlist_parser.MetadataAdapter()
        test_key = 'test_key'
        test_value = 'Test'
        test_metadata = {test_key: test_value}
        test_metadata_adapter._get_metadata = MagicMock(return_value=test_metadata)

        self.assertEqual(test_value, test_metadata_adapter.get(test_key))

    def test_when_load_metadata_is_called_then_metadata_is_updated_from_strategy(self):
        test_strategy = MagicMock()
        test_metadata_adapter = playlist_parser.MetadataAdapter(test_strategy)
        test_key = 'test_key'
        test_value = 'Test'
        test_metadata = {test_key: test_value}
        test_strategy.get_metadata = MagicMock(return_value=test_metadata)
        test_metadata_adapter._load_metadata_attempted = False

        self.assertEqual(test_value, test_metadata_adapter.get(test_key))


#   pylint: enable=unused-argument

if __name__ == '__main__':
    unittest.main()
