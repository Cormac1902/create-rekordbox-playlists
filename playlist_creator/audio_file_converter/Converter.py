import asyncio
import contextlib

from . import converter_strategy
from .ConverterContext import ConverterContext


#   pylint: disable=too-few-public-methods

class Converter:
    limit: asyncio.Semaphore
    transcodes_output_directory: str
    _converter_strategy: converter_strategy.ConverterStrategy

    def __init__(self,
                 limit: asyncio.Semaphore = None,
                 transcodes_output_directory=None,
                 _converter_strategy: converter_strategy.ConverterStrategy = None):
        self.__limit = limit
        self.transcodes_output_directory = transcodes_output_directory
        self._converter_strategy = _converter_strategy

    @property
    def _limit(self):
        return self.__limit if self.__limit else contextlib.nullcontext()

    async def convert_file(self, converter_context: ConverterContext):
        if self.__limit and self.__limit.locked():  # pragma: no cover
            print(f"Waiting to convert: {converter_context.playlist_entry.file()}", flush=True)

        async with self._limit:
            await converter_context.convert_playlist_entry(
                self._converter_strategy, self.transcodes_output_directory
            )

#   pylint: enable=too-few-public-methods
