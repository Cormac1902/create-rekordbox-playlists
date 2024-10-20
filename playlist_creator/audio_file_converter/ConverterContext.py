import logging
from dataclasses import dataclass

from playlist_creator import audio_file_converter, playlist_parser
from . import converter_strategy

logger = logging.getLogger(__name__)


@dataclass
class ConverterContext:
    playlist_entry: playlist_parser.PlaylistEntry
    retried: bool = False

    async def convert_playlist_entry(self,
                                     strategy: converter_strategy.ConverterStrategy,
                                     transcodes_output_directory):
        if audio_file_converter.ConversionType.NONE in self.playlist_entry.conversion_type():
            logging.debug(f"No processing needed for: {self.playlist_entry.file()}")
            return

        if not self.playlist_entry.metadata_successfully_loaded():
            return

        try:
            await strategy.convert_playlist_entry(
                self.playlist_entry, transcodes_output_directory
            )
        except converter_strategy.RetryQuietlyError as e:
            if self.retried:
                raise e

            self.retried = True
            logger.warning(f"Error converting {self.playlist_entry.file()}")
            [logger.debug(f"{p}={getattr(e, p)}") for p in dir(e) if not p.startswith('_')]
            logger.warning("Retrying quietly")
            await strategy.convert_playlist_entry(
                self.playlist_entry, transcodes_output_directory, True
            )
