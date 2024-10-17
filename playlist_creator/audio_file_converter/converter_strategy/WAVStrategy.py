import functools
import os
import pathlib

from ffmpeg.asyncio import FFmpeg

from playlist_creator import audio_file_converter, playlist_parser
from . import ffmpeg_composite
from .ConverterStrategy import ConverterStrategy, RetryQuietlyError


#   pylint: disable=too-few-public-methods

class WAVStrategy(ConverterStrategy):
    def __init__(self, converter_factory: ffmpeg_composite.ConverterFactory = None, **kwargs):
        super().__init__(**kwargs)
        self._converter_factory = converter_factory

    async def convert_playlist_entry(
            self,
            playlist_entry: playlist_parser.PlaylistEntry,
            transcodes_output_directory,
            quiet: bool = False
    ):
        ffmpeg = (
            FFmpeg()
            .option("y")
            .input(playlist_entry.file())
        )

        if quiet:
            ffmpeg = ffmpeg.option("v", "quiet").option("stats")

        converter = await self._prepare_converter(playlist_entry)
        transcoded_file = playlist_entry.transcoded_file(transcodes_output_directory)
        ffmpeg_output = converter.build_output(
            functools.partial(ffmpeg.output, url=transcoded_file)
        )
        ffmpeg = ffmpeg_output()

        pathlib.Path(os.path.split(transcoded_file)[0]).mkdir(parents=True, exist_ok=True)

        @ffmpeg.on("start")
        def on_start(_):
            print(f"{converter.message()}: {playlist_entry.file()}", flush=True)

        @ffmpeg.on("completed")
        def on_completed():
            print(f"Converted: {playlist_entry.file()}", flush=True)

        try:
            await ffmpeg.execute()
        except UnicodeDecodeError as e:
            raise RetryQuietlyError(e) from e

    async def _prepare_converter(
            self, playlist_entry: playlist_parser.PlaylistEntry
    ) -> ffmpeg_composite.Converter:
        converter = ffmpeg_composite.CompositeConverter()
        conversion_type = playlist_entry.conversion_type()

        if audio_file_converter.ConversionType.BIT_24 in conversion_type:
            converter.add(
                await self._converter_factory.get_converter(ffmpeg_composite.Bit24Converter)
            )

        if audio_file_converter.ConversionType.DOWNSAMPLE in conversion_type:
            converter.add(
                await self._converter_factory.get_converter(ffmpeg_composite.DownsampleConverter)
            )

        if audio_file_converter.ConversionType.WAV in conversion_type:
            converter.add(
                await self._converter_factory.get_converter(ffmpeg_composite.WAVConverter)
            )

        return converter

#   pylint: enable=too-few-public-methods
