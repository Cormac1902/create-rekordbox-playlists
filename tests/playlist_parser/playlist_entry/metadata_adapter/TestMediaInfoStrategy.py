from unittest.mock import MagicMock

from playlist_creator import playlist_parser


class TestMediaInfoStrategy(playlist_parser.IMediaInfoStrategy):
    def __init__(self, **kwargs):
        super().__init__('', **kwargs)
        self.get_metadata = MagicMock()

    def get_metadata(self, filename: str):
        pass
