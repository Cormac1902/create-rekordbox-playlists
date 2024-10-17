import functools

from ffmpeg.asyncio import FFmpeg

from .LeafConverter import LeafConverter


class WAVConverter(LeafConverter):
    def build_output(self, output: functools.partial) -> functools.partial[FFmpeg]:
        return output

    def message(self) -> str:
        return 'WAV'
