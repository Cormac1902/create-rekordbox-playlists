import unittest
from unittest.mock import MagicMock

from playlist_creator import audio_file_converter, playlist_parser
from .converter_strategy import TestConverterStrategy


class TestConverterContext(unittest.IsolatedAsyncioTestCase):
    async def test_when_convert_playlist_entry_is_called_then_converter_strategy_is_called(self):
        test_playlist_entry = playlist_parser.PlaylistEntry()
        test_playlist_entry.conversion_type = MagicMock()
        test_playlist_entry.metadata_successfully_loaded = MagicMock(return_value=True)
        test_converter_context = audio_file_converter.ConverterContext(test_playlist_entry)
        test_strategy = TestConverterStrategy()

        await test_converter_context.convert_playlist_entry(test_strategy, str())

        test_strategy.convert_playlist_entry.assert_called_once_with(test_playlist_entry, '')


if __name__ == '__main__':
    unittest.main()
