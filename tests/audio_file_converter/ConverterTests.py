import unittest
from unittest.mock import AsyncMock, MagicMock

from playlist_creator import audio_file_converter


class TestConverter(unittest.IsolatedAsyncioTestCase):
    async def test_when_convert_file_is_called_then_converter_context_is_called(self):
        test_context = audio_file_converter.ConverterContext(MagicMock())
        test_strategy = MagicMock()
        test_converter = audio_file_converter.Converter(
            transcodes_output_directory=str(), _converter_strategy=test_strategy
        )

        test_context.convert_playlist_entry = AsyncMock()

        await test_converter.convert_file(test_context)

        test_context.convert_playlist_entry.assert_called_once_with(test_strategy, '')


if __name__ == '__main__':
    unittest.main()
