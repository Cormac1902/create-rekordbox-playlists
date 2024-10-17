import functools
from ffmpeg.asyncio import FFmpeg
from abc import ABC, abstractmethod

class Converter(ABC):
    @abstractmethod
    def add(self, converter):
        pass

    @abstractmethod
    def build_output(self, output: functools.partial) -> functools.partial[FFmpeg]:
        pass

    @abstractmethod
    def message(self) -> str:
        pass

    @abstractmethod
    def remove(self, converter):
        pass
