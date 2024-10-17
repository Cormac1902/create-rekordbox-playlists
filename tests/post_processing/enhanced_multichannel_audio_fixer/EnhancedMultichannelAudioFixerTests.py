import unittest
import unittest.mock
from unittest.mock import MagicMock, call

from playlist_creator import audio_file_converter, playlist_parser, post_processing


class TestEnhancedMultichannelAudioFixer(unittest.TestCase):
    def test_when_process_is_called_file_is_edited(self):
        with unittest.mock.patch(
                "builtins.open", unittest.mock.mock_open(read_data=bytes())
        ) as mock_open:
            test_enhanced_multichannel_audio_fixer = post_processing.EnhancedMultichannelAudioFixer()
            test_playlist_entry = playlist_parser.PlaylistEntry()
            test_playlist_entry.metadata_successfully_loaded = MagicMock(return_value=True)
            test_playlist_entry.conversion_type = MagicMock(
                return_value=audio_file_converter.ConversionType.WAV
            )
            test_output_location = '/test/'
            test_playlist_entry.file_location = MagicMock(return_value=test_output_location)

            test_enhanced_multichannel_audio_fixer.process(test_playlist_entry, str())

            mock_open.assert_called_once_with(test_output_location, 'r+b')
            mock_open.return_value.seek.assert_has_calls([call(20), call(20)])
            mock_open.return_value.read.assert_called_once_with(2)
            mock_open.return_value.write.assert_called_once_with(bytes([0x01, 0x00]))


if __name__ == '__main__':
    unittest.main()
