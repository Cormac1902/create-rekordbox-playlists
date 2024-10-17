import functools

from ffmpeg.asyncio import FFmpeg

from .Converter import Converter


class CompositeConverter(Converter):
    def __init__(self):
        self._children = list[Converter]()

    def add(self, converter: Converter):
        self._children.append(converter)

    def build_output(self, output: functools.partial) -> functools.partial[FFmpeg]:
        for child in self._children:
            output = child.build_output(output)

        return output

    def message(self) -> str:
        return f"Converting to {' '.join([child.message() for child in self._children])}"

    def remove(self, converter: Converter):
        self._children.remove(converter)
