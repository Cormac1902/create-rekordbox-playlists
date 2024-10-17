import functools
from abc import abstractmethod

from ffmpeg.asyncio import FFmpeg

from .Converter import Converter


class LeafConverter(Converter):
    def add(self, converter):
        return NotImplemented

    @abstractmethod
    def build_output(self, output: functools.partial) -> functools.partial[FFmpeg]:
        pass

    @abstractmethod
    def message(self) -> str:
        pass

    def remove(self, converter):
        return NotImplemented
