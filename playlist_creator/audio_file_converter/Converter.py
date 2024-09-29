from ffmpeg.asyncio import FFmpeg
from pathlib import Path
from playlist_creator import audio_file_converter, playlist_parser

import asyncio
import os


async def _run_ffmpeg(ffmpeg: FFmpeg, output_location):
    Path(os.path.split(output_location)[0]).mkdir(parents=True, exist_ok=True)
    await ffmpeg.execute()


def _prepare_ffmpeg(playlist_entry: playlist_parser.PlaylistEntry, output_location: str) -> [FFmpeg, str]:
    ffmpeg = (
        FFmpeg()
        .option("y")
        .input(playlist_entry.file())
    )
    message = ''
    conversion_type = playlist_entry.conversion_type()

    if audio_file_converter.ConversionType.WAV in conversion_type:
        if audio_file_converter.ConversionType.BIT_24 in conversion_type:
            if audio_file_converter.ConversionType.DOWNSAMPLE in conversion_type:
                message = 'Converting to 24-bit 48kHz WAV'
                ffmpeg = ffmpeg.output(output_location, {"codec:a": "pcm_s24le"}, ar=48000)
            else:
                message = 'Converting to 24-bit WAV'
                ffmpeg = ffmpeg.output(output_location, {"codec:a": "pcm_s24le"})
        else:
            if audio_file_converter.ConversionType.DOWNSAMPLE in conversion_type:
                message = 'Converting to 48kHz WAV'
                ffmpeg = ffmpeg.output(output_location, ar=48000)
            else:
                message = 'Converting to WAV'
                ffmpeg = ffmpeg.output(output_location)
    elif conversion_type.DOWNSAMPLE in conversion_type:
        message = 'Downsampling'
        ffmpeg = ffmpeg.output(output_location, ar=48000)

    return ffmpeg, message


class Converter:
    limit: asyncio.Semaphore
    transcodes_output_directory: str

    def __init__(self, max_concurrent_tasks, transcodes_output_directory):
        self.limit = asyncio.Semaphore(max_concurrent_tasks)
        self.transcodes_output_directory = transcodes_output_directory

    async def convert_file(self, playlist_entry: playlist_parser.PlaylistEntry):
        if audio_file_converter.ConversionType.NONE in playlist_entry.conversion_type():
            print(f"No processing needed for: {playlist_entry.file()}")
            return

        output_location = playlist_entry.transcoded_file(self.transcodes_output_directory)

        if not os.path.isfile(output_location):
            (ffmpeg, message) = _prepare_ffmpeg(playlist_entry, output_location)

            async with self.limit:
                if self.limit.locked():
                    print(f"Waiting to convert: {playlist_entry.file()}")

                @ffmpeg.on("start")
                def on_start(_):
                    print(f"{message}: {playlist_entry.file()}")

                @ffmpeg.on("completed")
                def on_completed():
                    print(f"Converted:  {playlist_entry.file()}")

                await _run_ffmpeg(ffmpeg, output_location)
