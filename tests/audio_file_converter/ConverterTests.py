import unittest
from unittest.mock import AsyncMock, MagicMock

from playlist_creator import ConverterContext, audio_file_converter


class TestConverter(unittest.IsolatedAsyncioTestCase):
    async def test_when_convert_file_is_called_then_converter_context_is_called(self):
        test_context = ConverterContext(MagicMock())
        test_converter = audio_file_converter.Converter()

        test_context.convert_playlist_entry = AsyncMock()

        await test_converter.convert_file(test_context)

        test_context.convert_playlist_entry.assert_called_once()


if __name__ == '__main__':
    unittest.main()
