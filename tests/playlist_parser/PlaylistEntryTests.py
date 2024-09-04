from playlist_creator import ConversionType, playlist_parser
from _soundfile import ffi as _ffi
from unittest.mock import MagicMock

import os
import soundfile
import unittest


class TestPlaylistEntry(unittest.TestCase):
    def test_conversion_type_is_initialised_to_none(self):
        test_playlist_entry = playlist_parser.PlaylistEntry()

        self.assertEqual(ConversionType.NONE, test_playlist_entry.conversion_type)

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

    def test_get_metadata_returns_metadata(self):
        test_playlist_entry = playlist_parser.PlaylistEntry()

        test_metadata = test_playlist_entry.get_metadata()

        self.assertIsInstance(test_metadata, playlist_parser.PlaylistEntryMetadata)

    def test_processed_forwards_request_to_metadata(self):
        test_playlist_entry = playlist_parser.PlaylistEntry()
        test_metadata = playlist_parser.PlaylistEntryMetadata()

        test_metadata.contains_metadata = MagicMock(return_value=True)
        test_playlist_entry.get_metadata = MagicMock(return_value=test_metadata)

        self.assertTrue(test_playlist_entry.processed())
        test_metadata.contains_metadata.assert_called_once()

    def test_when_filename_is_none_transcoded_file_returns_empty_string(self):
        test_playlist_entry = playlist_parser.PlaylistEntry()

        self.assertEqual('', test_playlist_entry.transcoded_file(r'C:\test'))

    def test_when_filename_has_value_then_transcoded_file_returns_correctly(self):
        test_playlist_entry = playlist_parser.PlaylistEntry()
        test_metadata = playlist_parser.PlaylistEntryMetadata()

        test_filename = 'test'

        test_metadata.filename = MagicMock(return_value=test_filename)
        test_playlist_entry.get_metadata = MagicMock(return_value=test_metadata)

        test_output_directory = r'C:\test'

        self.assertEqual(
            os.path.join(test_output_directory, test_filename),
            test_playlist_entry.transcoded_file(test_output_directory)
        )

    def test_when_conversion_type_is_downsample_transcoded_file_returns_original_format(self):
        test_filename = 'test'
        test_file = f"{test_filename}.flac"
        test_playlist_entry = playlist_parser.PlaylistEntry(file=test_file)
        test_metadata = playlist_parser.PlaylistEntryMetadata()
        test_metadata.filename = MagicMock(return_value=test_filename)
        test_playlist_entry.get_metadata = MagicMock(return_value=test_metadata)

        test_playlist_entry.add_conversion_type(ConversionType.DOWNSAMPLE)

        self.assertEqual(test_file, test_playlist_entry.transcoded_file(''))

    def test_when_conversion_type_is_wav_transcoded_file_returns_wav(self):
        test_filename = 'test'
        test_playlist_entry = playlist_parser.PlaylistEntry(file=f"{test_filename}.flac")
        test_metadata = playlist_parser.PlaylistEntryMetadata()
        test_metadata.filename = MagicMock(return_value=test_filename)
        test_playlist_entry.get_metadata = MagicMock(return_value=test_metadata)

        test_playlist_entry.add_conversion_type(ConversionType.WAV)

        self.assertEqual(f"{test_filename}.wav", test_playlist_entry.transcoded_file(''))

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
        test_playlist_entry = playlist_parser.PlaylistEntry()
        test_playlist_entry.processed = MagicMock(return_value=True)
        soundfile.SoundFile = MagicMock(return_value=soundfile.SoundFile)
        test_soundfile = soundfile.SoundFile()
        test_soundfile.format = 'flac'

        test_playlist_entry.determine_conversion_type(['wav'], test_soundfile)

        self.assertIn(ConversionType.WAV, test_playlist_entry.conversion_type)

    def test_when_soundfile_format_is_allowed_conversion_type_is_none(self):
        test_playlist_entry = playlist_parser.PlaylistEntry()
        test_playlist_entry.processed = MagicMock(return_value=True)
        soundfile.SoundFile = MagicMock(return_value=soundfile.SoundFile)
        test_soundfile = soundfile.SoundFile()
        test_soundfile.format = 'mp3'

        test_playlist_entry.determine_conversion_type(['mp3'], test_soundfile)

        self.assertEqual(ConversionType.NONE, test_playlist_entry.conversion_type)

    def test_when_soundfile_samplerate_is_over_threshold_conversion_type_is_downsample(self):
        test_playlist_entry = playlist_parser.PlaylistEntry()
        test_playlist_entry.processed = MagicMock(return_value=True)
        soundfile.SoundFile = MagicMock(return_value=soundfile.SoundFile)
        test_soundfile = soundfile.SoundFile()
        test_soundfile.samplerate = 48001

        test_playlist_entry.determine_conversion_type(['wav'], test_soundfile)

        self.assertIn(ConversionType.DOWNSAMPLE, test_playlist_entry.conversion_type)

    def test_when_soundfile_subtype_is_PCM_24_conversion_type_is_BIT_24(self):
        test_playlist_entry = playlist_parser.PlaylistEntry()
        test_playlist_entry.processed = MagicMock(return_value=True)
        soundfile.SoundFile = MagicMock(return_value=soundfile.SoundFile)
        test_soundfile = soundfile.SoundFile()
        test_soundfile.subtype = 'PCM_24'

        test_playlist_entry.determine_conversion_type(['wav'], test_soundfile)

        self.assertIn(ConversionType.BIT_24, test_playlist_entry.conversion_type)


if __name__ == '__main__':
    unittest.main()
