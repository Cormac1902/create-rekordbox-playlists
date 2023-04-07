import os
from pathlib import WindowsPath

from ffmpeg.asyncio import FFmpeg

from ConversionTypeEnum import ConversionType
import PlaylistEntry


async def _run_ffmpeg(ffmpeg: FFmpeg, output_location):
    # TODO: Directories with . in the path
    WindowsPath("\\\\?\\" + os.path.split(output_location)[0]).mkdir(parents=True, exist_ok=True)
    # TODO: Filenames with " in the name
    await ffmpeg.execute()


async def convert(playlist_entry: PlaylistEntry, output_root):
    conversion_type = playlist_entry.conversion_type

    if ConversionType.NONE in conversion_type:
        print(playlist_entry.file)
        return

    print(playlist_entry.transcoded_file(output_root))

    output_location = playlist_entry.transcoded_file(output_root)
    ffmpeg = (
        FFmpeg()
        .option("y")
        .input(playlist_entry.file)
    )

    if ConversionType.WAV in conversion_type:
        if ConversionType.BIT_24 in conversion_type:
            if ConversionType.DOWNSAMPLE in conversion_type:
                ffmpeg = ffmpeg.output(output_location, {"codec:a": "pcm_s24le"}, ar=48000)
            else:
                ffmpeg = ffmpeg.output(output_location, {"codec:a": "pcm_s24le"})
        else:
            if ConversionType.DOWNSAMPLE in conversion_type:
                ffmpeg = ffmpeg.output(output_location, ar=48000)
            else:
                ffmpeg = ffmpeg.output(output_location)
    elif conversion_type.DOWNSAMPLE in conversion_type:
        ffmpeg = ffmpeg.output(output_location, ar=48000)

    output_location = playlist_entry.transcoded_file(output_root)

    await _run_ffmpeg(ffmpeg, output_location)
