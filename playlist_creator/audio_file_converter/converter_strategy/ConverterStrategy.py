#   pylint: disable=too-few-public-methods

from abc import ABC, abstractmethod

from playlist_creator import playlist_parser


class RetryQuietlyError(Exception):
    pass


class ConverterStrategy(ABC):
    @abstractmethod
    async def convert_playlist_entry(
            self,
            playlist_entry: playlist_parser.PlaylistEntry,
            transcodes_output_directory,
            quiet: bool = False
    ):
        pass

#   pylint: enable=too-few-public-methods
