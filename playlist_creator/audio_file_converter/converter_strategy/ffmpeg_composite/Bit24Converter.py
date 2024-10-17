import functools

from ffmpeg.asyncio import FFmpeg

from .LeafConverter import LeafConverter


class Bit24Converter(LeafConverter):
    def build_output(self, output: functools.partial) -> functools.partial[FFmpeg]:
        return functools.partial(output, options={"codec:a": "pcm_s24le"})

    def message(self) -> str:
        return '24-bit'
