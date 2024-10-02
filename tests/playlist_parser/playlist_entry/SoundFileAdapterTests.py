import os
import unittest
from unittest.mock import MagicMock

from playlist_creator import audio_file_converter, configuration, playlist_parser


class TestSoundFileAdapter(unittest.TestCase):
    def test_add_conversion_type_clears_none(self):
        test_soundfile_adapter = playlist_parser.SoundFileAdapter()

        test_soundfile_adapter.add_conversion_type(audio_file_converter.ConversionType.WAV)

        self.assertNotIn(audio_file_converter.ConversionType.NONE,
                         test_soundfile_adapter.conversion_type)

    def test_adding_none_conversion_type_clears_existing(self):
        test_soundfile_adapter = playlist_parser.SoundFileAdapter()

        test_soundfile_adapter.add_conversion_type(audio_file_converter.ConversionType.WAV)
        test_soundfile_adapter.add_conversion_type(audio_file_converter.ConversionType.NONE)

        self.assertEqual(audio_file_converter.ConversionType.NONE,
                         test_soundfile_adapter.conversion_type)

    def test_add_conversion_type_adds_conversion_type(self):
        test_soundfile_adapter = playlist_parser.SoundFileAdapter()

        test_soundfile_adapter.add_conversion_type(audio_file_converter.ConversionType.WAV)

        self.assertIn(audio_file_converter.ConversionType.WAV,
                      test_soundfile_adapter.conversion_type)

    def test_add_conversion_type_adds_multiple_conversion_types(self):
        test_soundfile_adapter = playlist_parser.SoundFileAdapter()

        test_soundfile_adapter.add_conversion_type(audio_file_converter.ConversionType.WAV)
        test_soundfile_adapter.add_conversion_type(audio_file_converter.ConversionType.BIT_24)

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
        test_soundfile_adapter._load_information_from_soundfile = MagicMock()

        test_soundfile_adapter._load_information()

        test_soundfile_adapter._load_information_from_soundfile.assert_not_called()

    def test_when_format_is_called_format_is_filled_from_soundfile(self):
        with unittest.mock.patch(
                'soundfile.SoundFile'
        ) as mock_soundfile:
            mock_soundfile.return_value.__enter__().format = 'mp3'
            test_soundfile_adapter = playlist_parser.SoundFileAdapter(
                config=configuration.Config(allowed_formats={'mp3'})
            )
            test_soundfile_adapter._load_information_attempted = False
            os.path.exists = MagicMock(return_value=True)

            self.assertEqual('mp3',test_soundfile_adapter.format)

    def test_when_soundfile_format_is_allowed_conversion_type_is_none(self):
        with unittest.mock.patch(
                'soundfile.SoundFile'
        ) as mock_soundfile:
            mock_soundfile.return_value.__enter__().format = 'mp3'
            test_soundfile_adapter = playlist_parser.SoundFileAdapter(
                config=configuration.Config(allowed_formats={'mp3'})
            )
            test_soundfile_adapter._load_information_attempted = False
            os.path.exists = MagicMock(return_value=True)

            self.assertEqual(audio_file_converter.ConversionType.NONE,
                             test_soundfile_adapter.conversion_type)

    def test_when_soundfile_format_is_not_allowed_conversion_type_contains_wav(self):
        with unittest.mock.patch(
                'soundfile.SoundFile'
        ) as mock_soundfile:
            mock_soundfile.return_value.__enter__().format = 'flac'
            test_soundfile_adapter = playlist_parser.SoundFileAdapter(
                config=configuration.Config(allowed_formats={'mp3'})
            )
            test_soundfile_adapter._load_information_attempted = False
            os.path.exists = MagicMock(return_value=True)

            self.assertIn(audio_file_converter.ConversionType.WAV,
                          test_soundfile_adapter.conversion_type)

    def test_when_soundfile_samplerate_is_over_threshold_conversion_type_is_downsample(self):
        with unittest.mock.patch(
                'soundfile.SoundFile'
        ) as mock_soundfile:
            mock_soundfile.return_value.__enter__().samplerate = 48001
            test_soundfile_adapter = playlist_parser.SoundFileAdapter()
            test_soundfile_adapter._load_information_attempted = False
            os.path.exists = MagicMock(return_value=True)

            self.assertIn(audio_file_converter.ConversionType.DOWNSAMPLE,
                          test_soundfile_adapter.conversion_type)

    def test_when_soundfile_subtype_is_PCM_24_conversion_type_is_BIT_24(self):
        with unittest.mock.patch(
                'soundfile.SoundFile'
        ) as mock_soundfile:
            mock_soundfile.return_value.__enter__().subtype = 'PCM_24'
            test_soundfile_adapter = playlist_parser.SoundFileAdapter()
            test_soundfile_adapter._load_information_attempted = False
            os.path.exists = MagicMock(return_value=True)

            self.assertIn(audio_file_converter.ConversionType.BIT_24,
                          test_soundfile_adapter.conversion_type)


if __name__ == '__main__':
    unittest.main()
