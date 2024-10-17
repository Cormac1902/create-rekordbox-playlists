#   pylint: disable=too-few-public-methods

import asyncio
import contextlib

from .Converter import Converter


class ConverterFactory:
    def __init__(self, lock: asyncio.Lock = None):
        self._converters: dict[Converter] = dict[Converter]()
        self.__lock = lock

    @property
    def _lock(self):
        return self.__lock if self.__lock else contextlib.nullcontext()

    async def get_converter(self, converter) -> Converter:
        async with self._lock:
            if converter not in self._converters:
                self._converters[converter] = converter()

        return self._converters[converter]

#   pylint: enable=too-few-public-methods
