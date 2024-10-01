#   pylint: disable=protected-access

import os
import unittest
from unittest.mock import MagicMock, PropertyMock, patch

import soundfile

from playlist_creator import audio_file_converter, configuration, playlist_parser


class TestPlaylistEntry(unittest.TestCase):
    def test_lock_is_initialised(self):
        test_lock = MagicMock()
        test_playlist_entry = playlist_parser.PlaylistEntry(test_lock)

        self.assertEqual(test_playlist_entry._lock, test_lock)

    def test_metadata_adapter_is_initialised(self):
        test_metadata_adapter = playlist_parser.MetadataAdapter()
        playlist_parser.metadata_adapter.MetadataAdapter = MagicMock(
            return_value=test_metadata_adapter
        )
        test_media_info_strategy_factory = MagicMock()
        test_media_info_strategy_factory.get_strategy = MagicMock(
            return_value=test_metadata_adapter
        )
        test_playlist_entry = playlist_parser.PlaylistEntry(
            media_info_strategy_factory=test_media_info_strategy_factory
        )
        test_playlist_entry.conversion_type = MagicMock(
            return_value=audio_file_converter.ConversionType.NONE)
        test_playlist_entry.format = MagicMock(return_value='WAV')

        self.assertEqual(test_playlist_entry._metadata_adapter(), test_metadata_adapter)
        playlist_parser.metadata_adapter.MetadataAdapter.assert_called_once()

    @patch.object(
        playlist_parser.metadata_adapter.MetadataAdapter,
        'contains_metadata',
        new_callable=PropertyMock(return_value=True)
    )
    def test_metadata_successfully_loaded_forwards_requests_to_metadata_adapter(self,
                                                                                contains_metadata):
        test_playlist_entry = playlist_parser.PlaylistEntry()
        test_metadata_adapter = playlist_parser.MetadataAdapter()
        playlist_parser.metadata_adapter.MetadataAdapter = MagicMock(
            return_value=test_metadata_adapter
        )

        self.assertTrue(test_playlist_entry.metadata_successfully_loaded())

    def test_file_returns_from_playlist_entry_data(self):
        test_length = '100'
        test_playlist_entry_data = playlist_parser.PlaylistEntryData(length=test_length)
        test_playlist_entry = playlist_parser.PlaylistEntry(
            playlist_entry_data=test_playlist_entry_data
        )

        self.assertEqual(test_playlist_entry.length(), test_length)

    def test_title_returns_from_playlist_entry_data(self):
        test_title = 'Test Title'
        test_playlist_entry_data = playlist_parser.PlaylistEntryData(title=test_title)
        test_playlist_entry = playlist_parser.PlaylistEntry(
            playlist_entry_data=test_playlist_entry_data
        )

        self.assertEqual(test_playlist_entry.title(), test_title)

    def test_when_conversion_type_is_none_conversion_type_is_none_returns_true(self):
        test_playlist_entry = playlist_parser.PlaylistEntry()
        test_playlist_entry.conversion_type = MagicMock(
            return_value=audio_file_converter.ConversionType.NONE
        )

        self.assertTrue(test_playlist_entry.conversion_type_is_none())

    def test_when_conversion_type_is_not_none_conversion_type_is_none_returns_false(self):
        test_playlist_entry = playlist_parser.PlaylistEntry()
        test_playlist_entry.conversion_type = MagicMock(
            return_value=audio_file_converter.ConversionType.WAV
        )

        self.assertFalse(test_playlist_entry.conversion_type_is_none())

    def test_when_conversion_type_is_none_file_location_returns_original_file(self):
        test_file = 'test'
        test_playlist_entry = playlist_parser.PlaylistEntry(
            playlist_entry_data=playlist_parser.PlaylistEntryData(test_file)
        )
        test_playlist_entry.conversion_type = MagicMock(
            return_value=audio_file_converter.ConversionType
        )

        self.assertEqual(test_file, test_playlist_entry.file_location(''))

    def test_when_conversion_type_is_not_none_file_location_returns_transcoded_file(self):
        test_file = 'test'
        test_playlist_entry = playlist_parser.PlaylistEntry()
        test_playlist_entry.conversion_type = MagicMock(return_value=audio_file_converter.ConversionType.WAV)
        test_playlist_entry.transcoded_file = MagicMock(return_value=test_file)

        self.assertEqual(test_file, test_playlist_entry.file_location(''))

    def test_transcoded_file_exists_calls_os_path_isfile(self):
        test_transcoded_file = 'test.flac'
        test_playlist_entry = playlist_parser.PlaylistEntry()
        os.path.isfile = MagicMock(return_value=True)
        test_playlist_entry.transcoded_file = MagicMock(return_value=test_transcoded_file)

        test_playlist_entry.transcoded_file_exists('')
        os.path.isfile.assert_called_with(test_transcoded_file)

    def test_when_transcoded_file_exists_then_transcoded_file_exists_returns_true(self):
        test_transcoded_file = 'test.flac'
        test_playlist_entry = playlist_parser.PlaylistEntry()
        os.path.isfile = MagicMock(return_value=True)
        test_playlist_entry.transcoded_file = MagicMock(return_value=test_transcoded_file)

        self.assertTrue(test_playlist_entry.transcoded_file_exists(''))

    def test_when_transcoded_file_does_not_exist_then_transcoded_file_exists_returns_false(self):
        test_transcoded_file = 'test.flac'
        test_playlist_entry = playlist_parser.PlaylistEntry()
        os.path.isfile = MagicMock(return_value=False)
        test_playlist_entry.transcoded_file = MagicMock(return_value=test_transcoded_file)

        self.assertFalse(test_playlist_entry.transcoded_file_exists(''))


    def test_get_metadata_forwards_requests_to_metadata_adapter(self):
        test_metadata_adapter = playlist_parser.MetadataAdapter()
        playlist_parser.metadata_adapter.MetadataAdapter = MagicMock(
            return_value=test_metadata_adapter
        )
        test_playlist_entry = playlist_parser.PlaylistEntry()
        test_metadata_adapter.load_metadata = MagicMock()

        test_playlist_entry.get_metadata()

        test_metadata_adapter.load_metadata.assert_called_once()

    def test_get_metadata_tag_forwards_requests_to_metadata_adapter(self):
        test_metadata_adapter = playlist_parser.MetadataAdapter()
        playlist_parser.metadata_adapter.MetadataAdapter = MagicMock(
            return_value=test_metadata_adapter
        )
        test_playlist_entry = playlist_parser.PlaylistEntry()
        test_key = 'test_key'
        test_value = 'test'
        test_dict = {test_key: test_value}
        test_metadata_adapter.get = MagicMock(side_effect=test_dict.get)

        self.assertEqual(test_value, test_playlist_entry.get_metadata_tag(test_key))
        test_metadata_adapter.get.assert_called_once()

    def test_when_filename_is_none_transcoded_file_returns_empty_string(self):
        test_playlist_entry = playlist_parser.PlaylistEntry(media_info_strategy_factory=MagicMock())
        test_metadata_adapter = playlist_parser.MetadataAdapter()
        playlist_parser.metadata_adapter.MetadataAdapter = MagicMock(
            return_value=test_metadata_adapter
        )

        self.assertEqual('', test_playlist_entry.transcoded_file(r'C:\test'))

    def test_when_filename_has_value_then_transcoded_file_returns_correctly(self):
        test_playlist_entry = playlist_parser.PlaylistEntry()
        test_metadata_adapter = playlist_parser.MetadataAdapter()

        test_filename = 'test'

        test_metadata_adapter.formatted_filename = MagicMock(return_value=test_filename)
        playlist_parser.metadata_adapter.MetadataAdapter = MagicMock(
            return_value=test_metadata_adapter
        )
        test_playlist_entry.conversion_type = MagicMock(
            return_value=audio_file_converter.ConversionType.NONE
        )

        test_output_directory = r'C:\test'

        self.assertEqual(
            os.path.join(test_output_directory, test_filename),
            test_playlist_entry.transcoded_file(test_output_directory)
        )

    def test_when_conversion_type_is_downsample_transcoded_file_returns_original_format(self):
        test_filename = 'test'
        test_file = f"{test_filename}.flac"
        test_playlist_entry = playlist_parser.PlaylistEntry(
            playlist_entry_data=playlist_parser.PlaylistEntryData(test_file)
        )
        test_metadata_adapter = playlist_parser.MetadataAdapter()
        test_metadata_adapter.formatted_filename = MagicMock(return_value=test_filename)
        playlist_parser.metadata_adapter.MetadataAdapter = MagicMock(
            return_value=test_metadata_adapter
        )
        test_playlist_entry.conversion_type = MagicMock(
            return_value=audio_file_converter.ConversionType.DOWNSAMPLE
        )

        self.assertEqual(test_file, test_playlist_entry.transcoded_file(''))

    def test_when_conversion_type_is_wav_transcoded_file_returns_wav(self):
        test_filename = 'test'
        test_playlist_entry = playlist_parser.PlaylistEntry(
            playlist_entry_data=playlist_parser.PlaylistEntryData(f"{test_filename}.flac")
        )
        test_metadata_adapter = playlist_parser.MetadataAdapter()
        test_metadata_adapter.formatted_filename = MagicMock(return_value=test_filename)
        playlist_parser.metadata_adapter.MetadataAdapter = MagicMock(
            return_value=test_metadata_adapter
        )
        test_playlist_entry.conversion_type = MagicMock(
            return_value=audio_file_converter.ConversionType.WAV)

        self.assertEqual(f"{test_filename}.wav", test_playlist_entry.transcoded_file(''))

    def test_equals(self):
        test_playlist_entry = playlist_parser.PlaylistEntry()

        self.assertFalse(test_playlist_entry == {})

    def test_hash(self):
        test_playlist_entry = playlist_parser.PlaylistEntry()

        self.assertEqual({test_playlist_entry}, {playlist_parser.PlaylistEntry()})


if __name__ == '__main__':
    unittest.main()
