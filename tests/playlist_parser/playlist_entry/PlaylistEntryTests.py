#   pylint: disable=protected-access

import os
import unittest
from unittest.mock import MagicMock

import soundfile

from playlist_creator import ConversionType, configuration, playlist_parser


class TestPlaylistEntry(unittest.TestCase):
    def test_conversion_type_is_initialised_to_none(self):
        test_playlist_entry = playlist_parser.PlaylistEntry()

        self.assertEqual(ConversionType.NONE, test_playlist_entry.conversion_type())

    def test_lock_is_initialised(self):
        test_lock = MagicMock()
        test_playlist_entry = playlist_parser.PlaylistEntry(test_lock)

        self.assertEqual(test_playlist_entry._lock, test_lock)

    def test_media_info_adapter_is_initialised(self):
        test_media_info_adapter = playlist_parser.MediaInfoAdapter()

        with unittest.mock.patch(
                'playlist_creator.playlist_parser.playlist_entry.PlaylistEntry.MediaInfoAdapter'
        ) as mock_media_info_adapter:
            test_manager = MagicMock()
            mock_media_info_adapter.return_value = test_media_info_adapter
            test_playlist_entry = playlist_parser.PlaylistEntry(test_manager)

            mock_media_info_adapter.assert_called_once()
            self.assertEqual(test_playlist_entry._media_info_adapter, test_media_info_adapter)

    def test_metadata_successfully_loaded_forwards_requests_to_media_info_adapter(self):
        test_playlist_entry = playlist_parser.PlaylistEntry()
        test_media_info_adapter = playlist_parser.MediaInfoAdapter()

        test_media_info_adapter.contains_metadata = MagicMock(return_value=True)

        test_playlist_entry._media_info_adapter = test_media_info_adapter

        self.assertTrue(test_playlist_entry.metadata_successfully_loaded())
        test_media_info_adapter.contains_metadata.assert_called_once()

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

    def test_add_conversion_type_clears_none(self):
        test_playlist_entry = playlist_parser.PlaylistEntry()

        test_playlist_entry.add_conversion_type(ConversionType.WAV)

        self.assertNotIn(ConversionType.NONE, test_playlist_entry.conversion_type())

    def test_adding_none_conversion_type_clears_existing(self):
        test_playlist_entry = playlist_parser.PlaylistEntry()

        test_playlist_entry.add_conversion_type(ConversionType.WAV)
        test_playlist_entry.add_conversion_type(ConversionType.NONE)

        self.assertEqual(ConversionType.NONE, test_playlist_entry.conversion_type())

    def test_add_conversion_type_adds_conversion_type(self):
        test_playlist_entry = playlist_parser.PlaylistEntry()

        test_playlist_entry.add_conversion_type(ConversionType.WAV)

        self.assertIn(ConversionType.WAV, test_playlist_entry.conversion_type())

    def test_add_conversion_type_adds_multiple_conversion_types(self):
        test_playlist_entry = playlist_parser.PlaylistEntry()

        test_playlist_entry.add_conversion_type(ConversionType.WAV)
        test_playlist_entry.add_conversion_type(ConversionType.BIT_24)

        self.assertIn(ConversionType.WAV, test_playlist_entry.conversion_type())
        self.assertIn(ConversionType.BIT_24, test_playlist_entry.conversion_type())

    def test_when_conversion_type_is_none_file_location_returns_original_file(self):
        test_file = 'test'
        test_playlist_entry = playlist_parser.PlaylistEntry(
            playlist_entry_data=playlist_parser.PlaylistEntryData(test_file)
        )

        self.assertEqual(test_file, test_playlist_entry.file_location(''))

    def test_when_conversion_type_is_not_none_file_location_returns_transcoded_file(self):
        test_file = 'test'
        test_playlist_entry = playlist_parser.PlaylistEntry()
        test_playlist_entry.transcoded_file = MagicMock(return_value=test_file)

        test_playlist_entry.add_conversion_type(ConversionType.WAV)

        self.assertEqual(test_file, test_playlist_entry.file_location(''))

    def test_when_soundfile_format_is_not_allowed_conversion_type_contains_wav(self):
        with unittest.mock.patch(
                'soundfile.SoundFile'
        ) as mock_soundfile:
            mock_soundfile.return_value.__enter__().format = 'flac'
            test_playlist_entry = playlist_parser.PlaylistEntry(
                config=configuration.Config(allowed_formats={'wav'})
            )
            test_playlist_entry.metadata_successfully_loaded = MagicMock(return_value=True)

            self.assertIn(ConversionType.WAV, test_playlist_entry.conversion_type())

    def test_when_soundfile_format_is_allowed_conversion_type_is_none(self):
        with unittest.mock.patch(
                'soundfile.SoundFile'
        ) as mock_soundfile:
            mock_soundfile.return_value.__enter__().format = 'mp3'
            test_playlist_entry = playlist_parser.PlaylistEntry(
                config=configuration.Config(allowed_formats={'mp3'})
            )
            test_playlist_entry.metadata_successfully_loaded = MagicMock(return_value=True)

            self.assertEqual(ConversionType.NONE, test_playlist_entry.conversion_type())

    def test_when_soundfile_samplerate_is_over_threshold_conversion_type_is_downsample(self):
        with unittest.mock.patch(
                'soundfile.SoundFile'
        ) as mock_soundfile:
            mock_soundfile.return_value.__enter__().samplerate = 48001
            test_playlist_entry = playlist_parser.PlaylistEntry(
                config=configuration.Config(allowed_formats={'wav'})
            )
            test_playlist_entry.metadata_successfully_loaded = MagicMock(return_value=True)

            self.assertIn(ConversionType.DOWNSAMPLE, test_playlist_entry.conversion_type())

    def test_when_soundfile_subtype_is_PCM_24_conversion_type_is_BIT_24(self):
        with unittest.mock.patch(
                'soundfile.SoundFile'
        ) as mock_soundfile:
            mock_soundfile.return_value.__enter__().subtype = 'PCM_24'
            test_playlist_entry = playlist_parser.PlaylistEntry(
                config=configuration.Config(allowed_formats={'wav'})
            )
            test_playlist_entry.metadata_successfully_loaded = MagicMock(return_value=True)

            self.assertIn(ConversionType.BIT_24, test_playlist_entry.conversion_type())

    def test_get_metadata_tag_forwards_requests_to_media_info_adapter(self):
        test_playlist_entry = playlist_parser.PlaylistEntry()
        test_media_info_adapter = playlist_parser.MediaInfoAdapter()
        test_value = 'test'
        test_media_info_adapter.get = MagicMock(return_value=test_value)

        test_playlist_entry._media_info_adapter = test_media_info_adapter

        self.assertEqual(test_playlist_entry.get_metadata_tag(''), test_value)
        test_media_info_adapter.get.assert_called_once()

    def test_when_filename_is_none_transcoded_file_returns_empty_string(self):
        test_playlist_entry = playlist_parser.PlaylistEntry()

        self.assertEqual('', test_playlist_entry.transcoded_file(r'C:\test'))

    def test_when_filename_has_value_then_transcoded_file_returns_correctly(self):
        test_playlist_entry = playlist_parser.PlaylistEntry()
        test_media_info_adapter = playlist_parser.MediaInfoAdapter()

        test_filename = 'test'

        test_media_info_adapter.formatted_filename = MagicMock(return_value=test_filename)
        test_playlist_entry._media_info_adapter = test_media_info_adapter

        test_output_directory = r'C:\test'

        self.assertEqual(
            os.path.join(test_output_directory, test_filename),
            test_playlist_entry.transcoded_file(test_output_directory)
        )

    def test_when_conversion_type_is_called_twice_then_soundfile_is_only_called_once(self):
        test_playlist_entry = playlist_parser.PlaylistEntry()
        test_playlist_entry.metadata_successfully_loaded = MagicMock(return_value=True)
        soundfile.SoundFile = MagicMock()

        test_playlist_entry.conversion_type()
        test_playlist_entry.conversion_type()

        soundfile.SoundFile.assert_called_once()

    def test_when_conversion_type_is_downsample_transcoded_file_returns_original_format(self):
        test_filename = 'test'
        test_file = f"{test_filename}.flac"
        test_playlist_entry = playlist_parser.PlaylistEntry(
            playlist_entry_data=playlist_parser.PlaylistEntryData(test_file)
        )
        test_media_info_adapter = playlist_parser.MediaInfoAdapter()
        test_media_info_adapter.formatted_filename = MagicMock(return_value=test_filename)
        test_playlist_entry._media_info_adapter = test_media_info_adapter

        test_playlist_entry.add_conversion_type(ConversionType.DOWNSAMPLE)

        self.assertEqual(test_file, test_playlist_entry.transcoded_file(''))

    def test_when_conversion_type_is_wav_transcoded_file_returns_wav(self):
        test_filename = 'test'
        test_playlist_entry = playlist_parser.PlaylistEntry(
            playlist_entry_data=playlist_parser.PlaylistEntryData(f"{test_filename}.flac")
        )
        test_media_info_adapter = playlist_parser.MediaInfoAdapter()
        test_media_info_adapter.formatted_filename = MagicMock(return_value=test_filename)
        test_playlist_entry._media_info_adapter = test_media_info_adapter

        test_playlist_entry.add_conversion_type(ConversionType.WAV)

        self.assertEqual(f"{test_filename}.wav", test_playlist_entry.transcoded_file(''))

    def test_equals(self):
        test_playlist_entry = playlist_parser.PlaylistEntry()

        self.assertFalse(test_playlist_entry == {})

    def test_hash(self):
        test_playlist_entry = playlist_parser.PlaylistEntry()

        self.assertEqual({test_playlist_entry}, {playlist_parser.PlaylistEntry()})


if __name__ == '__main__':
    unittest.main()
