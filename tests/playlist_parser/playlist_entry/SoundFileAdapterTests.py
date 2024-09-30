import unittest
from unittest.mock import MagicMock, Mock

from playlist_creator import audio_file_converter, playlist_parser


class TestSoundFileAdapter(unittest.TestCase):
    def test_add_conversion_type_clears_none(self):
        test_soundfile_adapter = playlist_parser.SoundFileAdapter()

        test_soundfile_adapter.add_conversion_type(audio_file_converter.ConversionType.WAV)
        test_soundfile_adapter._load_conversion_type_attempted = True

        self.assertNotIn(audio_file_converter.ConversionType.NONE,
                         test_soundfile_adapter.conversion_type)

    def test_adding_none_conversion_type_clears_existing(self):
        test_soundfile_adapter = playlist_parser.SoundFileAdapter()

        test_soundfile_adapter.add_conversion_type(audio_file_converter.ConversionType.WAV)
        test_soundfile_adapter.add_conversion_type(audio_file_converter.ConversionType.NONE)
        test_soundfile_adapter._load_conversion_type_attempted = True

        self.assertEqual(audio_file_converter.ConversionType.NONE,
                         test_soundfile_adapter.conversion_type)

    def test_add_conversion_type_adds_conversion_type(self):
        test_soundfile_adapter = playlist_parser.SoundFileAdapter()

        test_soundfile_adapter.add_conversion_type(audio_file_converter.ConversionType.WAV)
        test_soundfile_adapter._load_conversion_type_attempted = True

        self.assertIn(audio_file_converter.ConversionType.WAV,
                      test_soundfile_adapter.conversion_type)

    def test_add_conversion_type_adds_multiple_conversion_types(self):
        test_soundfile_adapter = playlist_parser.SoundFileAdapter()

        test_soundfile_adapter.add_conversion_type(audio_file_converter.ConversionType.WAV)
        test_soundfile_adapter.add_conversion_type(audio_file_converter.ConversionType.BIT_24)
        test_soundfile_adapter._load_conversion_type_attempted = True

        self.assertIn(audio_file_converter.ConversionType.WAV,
                      test_soundfile_adapter.conversion_type)
        self.assertIn(audio_file_converter.ConversionType.BIT_24,
                      test_soundfile_adapter.conversion_type)

    def test_conversion_type_is_initialised_to_none(self):
        test_soundfile_adapter = playlist_parser.SoundFileAdapter()

        self.assertEqual(audio_file_converter.ConversionType.NONE,
                         test_soundfile_adapter.conversion_type)

    def test_when_load_information_attempted_is_true_then_load_information_returns(self):
        test_soundfile_adapter = playlist_parser.SoundFileAdapter()
        test_soundfile_adapter._load_conversion_type_attempted = True
        test_soundfile_adapter._load_information_from_soundfile = MagicMock()

        test_soundfile_adapter._load_information()

        test_soundfile_adapter._load_information_from_soundfile.assert_not_called()


if __name__ == '__main__':
    unittest.main()
