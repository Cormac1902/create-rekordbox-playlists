from unittest.mock import AsyncMock

from playlist_creator import audio_file_converter, playlist_parser


#   pylint: disable=too-few-public-methods

class TestConverterStrategy(audio_file_converter.ConverterStrategy):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.convert_playlist_entry = AsyncMock()

    async def convert_playlist_entry(
            self,
            playlist_entry: playlist_parser.PlaylistEntry,
            transcodes_output_directory,
            quiet: bool = False
    ):
        pass

#   pylint: enable=too-few-public-methods
