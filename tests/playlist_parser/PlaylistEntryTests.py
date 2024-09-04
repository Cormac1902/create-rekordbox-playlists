from playlist_creator import ConversionType, playlist_parser
from unittest.mock import MagicMock, PropertyMock

import os
import soundfile
import unittest


class TestPlaylistEntry(unittest.TestCase):
    def test_conversion_type_is_initialised_to_none(self):
        test_playlist_entry = playlist_parser.PlaylistEntry()

        self.assertEqual(ConversionType.NONE, test_playlist_entry.conversion_type)

    def test_metadata_successfully_loaded_forwards_requests_to_media_info_adapter(self):
        test_playlist_entry = playlist_parser.PlaylistEntry()
        test_media_info_adapter = playlist_parser.MediaInfoAdapter()

        test_media_info_adapter.contains_metadata = MagicMock(return_value=True)

        test_playlist_entry._media_info_adapter = test_media_info_adapter

        self.assertTrue(test_playlist_entry.metadata_successfully_loaded)
        test_media_info_adapter.contains_metadata.assert_called_once()

    def test_add_conversion_type_clears_none(self):
        test_playlist_entry = playlist_parser.PlaylistEntry()

        test_playlist_entry.add_conversion_type(ConversionType.WAV)

        self.assertNotIn(ConversionType.NONE, test_playlist_entry.conversion_type)

    def test_adding_none_conversion_type_clears_existing(self):
        test_playlist_entry = playlist_parser.PlaylistEntry()

        test_playlist_entry.add_conversion_type(ConversionType.WAV)
        test_playlist_entry.add_conversion_type(ConversionType.NONE)

        self.assertEqual(ConversionType.NONE, test_playlist_entry.conversion_type)

    def test_add_conversion_type_adds_conversion_type(self):
        test_playlist_entry = playlist_parser.PlaylistEntry()

        test_playlist_entry.add_conversion_type(ConversionType.WAV)

        self.assertIn(ConversionType.WAV, test_playlist_entry.conversion_type)

    def test_add_conversion_type_adds_multiple_conversion_types(self):
        test_playlist_entry = playlist_parser.PlaylistEntry()

        test_playlist_entry.add_conversion_type(ConversionType.WAV)
        test_playlist_entry.add_conversion_type(ConversionType.BIT_24)

        self.assertIn(ConversionType.WAV, test_playlist_entry.conversion_type)
        self.assertIn(ConversionType.BIT_24, test_playlist_entry.conversion_type)

    def test_when_conversion_type_is_none_file_location_returns_original_file(self):
        test_file = 'test'
        test_playlist_entry = playlist_parser.PlaylistEntry(file=test_file)

        self.assertEqual(test_file, test_playlist_entry.file_location(''))

    def test_when_conversion_type_is_not_none_file_location_returns_transcoded_file(self):
        test_file = 'test'
        test_playlist_entry = playlist_parser.PlaylistEntry()
        test_playlist_entry.transcoded_file = MagicMock(return_value=test_file)

        test_playlist_entry.add_conversion_type(ConversionType.WAV)

        self.assertEqual(test_file, test_playlist_entry.file_location(''))

    def test_when_soundfile_format_is_not_allowed_conversion_type_contains_wav(self):
        with unittest.mock.patch('playlist_creator.PlaylistEntry.metadata_successfully_loaded',
                                 new_callable=PropertyMock) as mock_metadata_successfully_loaded:
            mock_metadata_successfully_loaded.return_value = True
            test_playlist_entry = playlist_parser.PlaylistEntry()
            soundfile.SoundFile = MagicMock(return_value=soundfile.SoundFile)
            soundfile.SoundFile().format = 'flac'

            test_playlist_entry.get_conversion_type(['wav'])

            self.assertIn(ConversionType.WAV, test_playlist_entry.conversion_type)

    def test_when_soundfile_format_is_allowed_conversion_type_is_none(self):
        with unittest.mock.patch('playlist_creator.PlaylistEntry.metadata_successfully_loaded',
                                 new_callable=PropertyMock) as mock_metadata_successfully_loaded:
            mock_metadata_successfully_loaded.return_value = True
            test_playlist_entry = playlist_parser.PlaylistEntry()
            soundfile.SoundFile = MagicMock(return_value=soundfile.SoundFile)
            soundfile.SoundFile().format = 'mp3'

            test_playlist_entry.get_conversion_type(['mp3'])

            self.assertEqual(ConversionType.NONE, test_playlist_entry.conversion_type)

    def test_when_soundfile_samplerate_is_over_threshold_conversion_type_is_downsample(self):
        with unittest.mock.patch('playlist_creator.PlaylistEntry.metadata_successfully_loaded',
                                 new_callable=PropertyMock) as mock_metadata_successfully_loaded:
            mock_metadata_successfully_loaded.return_value = True
            test_playlist_entry = playlist_parser.PlaylistEntry()
            soundfile.SoundFile = MagicMock(return_value=soundfile.SoundFile)
            soundfile.SoundFile().samplerate = 48001

            test_playlist_entry.get_conversion_type(['wav'])

            self.assertIn(ConversionType.DOWNSAMPLE, test_playlist_entry.conversion_type)

    def test_when_soundfile_subtype_is_PCM_24_conversion_type_is_BIT_24(self):
        with unittest.mock.patch('playlist_creator.PlaylistEntry.metadata_successfully_loaded',
                                 new_callable=PropertyMock) as mock_metadata_successfully_loaded:
            mock_metadata_successfully_loaded.return_value = True
            test_playlist_entry = playlist_parser.PlaylistEntry()
            soundfile.SoundFile = MagicMock(return_value=soundfile.SoundFile)
            soundfile.SoundFile().subtype = 'PCM_24'

            test_playlist_entry.get_conversion_type(['wav'])

            self.assertIn(ConversionType.BIT_24, test_playlist_entry.conversion_type)

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

    def test_when_conversion_type_is_downsample_transcoded_file_returns_original_format(self):
        test_filename = 'test'
        test_file = f"{test_filename}.flac"
        test_playlist_entry = playlist_parser.PlaylistEntry(file=test_file)
        test_media_info_adapter = playlist_parser.MediaInfoAdapter()
        test_media_info_adapter.formatted_filename = MagicMock(return_value=test_filename)
        test_playlist_entry._media_info_adapter = test_media_info_adapter

        test_playlist_entry.add_conversion_type(ConversionType.DOWNSAMPLE)

        self.assertEqual(test_file, test_playlist_entry.transcoded_file(''))

    def test_when_conversion_type_is_wav_transcoded_file_returns_wav(self):
        test_filename = 'test'
        test_playlist_entry = playlist_parser.PlaylistEntry(file=f"{test_filename}.flac")
        test_media_info_adapter = playlist_parser.MediaInfoAdapter()
        test_media_info_adapter.formatted_filename = MagicMock(return_value=test_filename)
        test_playlist_entry._media_info_adapter = test_media_info_adapter

        test_playlist_entry.add_conversion_type(ConversionType.WAV)

        self.assertEqual(f"{test_filename}.wav", test_playlist_entry.transcoded_file(''))


if __name__ == '__main__':
    unittest.main()
