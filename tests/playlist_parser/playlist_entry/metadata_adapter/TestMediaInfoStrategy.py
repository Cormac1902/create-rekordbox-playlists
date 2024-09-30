from unittest.mock import MagicMock

from playlist_creator import playlist_parser


class TestMediaInfoStrategy(playlist_parser.IMediaInfoStrategy):
    def __init__(self, **kwargs):
        super().__init__('', **kwargs)
        self.get_metadata = MagicMock()

    def _get_cmd(self, filename: str):
        pass

    def _get_metadata_from_cmd(self, cmd_output: str) -> dict:
        pass


class ConcreteTestMediaInfoStrategy(playlist_parser.IMediaInfoStrategy):
    def __init__(self, **kwargs):
        super().__init__('', **kwargs)
        self._get_cmd = MagicMock()
        self._get_metadata_from_cmd = MagicMock()

    def _get_cmd(self, filename: str):
        pass

    def _get_metadata_from_cmd(self, cmd_output: str) -> dict:
        pass
