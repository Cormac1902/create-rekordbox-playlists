import functools

from ffmpeg.asyncio import FFmpeg

from .LeafConverter import LeafConverter


class DownsampleConverter(LeafConverter):
    def build_output(self, output: functools.partial) -> functools.partial[FFmpeg]:
        return functools.partial(output, ar=48000)

    def message(self) -> str:
        return '48kHz'
