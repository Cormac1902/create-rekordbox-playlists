import os
from pathlib import Path

import taglib
from ffmpeg.asyncio import FFmpeg

from ConversionTypeEnum import ConversionType
from MediaInfoMetadata import MediaInfoMetadata, TAGS_TO_LOAD
from PlaylistEntry import PlaylistEntry
from PlaylistEntryMetadata import PlaylistEntryMetadata


async def _run_ffmpeg(ffmpeg: FFmpeg, output_location):
    Path(os.path.split(output_location)[0]).mkdir(parents=True, exist_ok=True)
    await ffmpeg.execute()


def _copy_tag(file: taglib.File, tag: str, metadata: MediaInfoMetadata, make_list=True):
    metadata_tag = metadata.get(tag)
    if metadata_tag:
        file.tags[tag] = [metadata_tag] if make_list else metadata_tag.split(';')


async def _tag(metadata: PlaylistEntryMetadata, output_location):
    print(f"Updating tags: {output_location}")
    with taglib.File(output_location, save_on_exit=True) as file:
        for tag in TAGS_TO_LOAD:
            _copy_tag(file, tag, metadata.raw_metadata, tag not in ['artist', 'genre', 'producer'])


async def convert(playlist_entry: PlaylistEntry, output_root):
    conversion_type = playlist_entry.conversion_type

    if ConversionType.NONE in conversion_type:
        print(f"No processing needed for: {playlist_entry.file}")
        return

    output_location = playlist_entry.transcoded_file(output_root)

    if not os.path.isfile(output_location):
        ffmpeg = (
            FFmpeg()
            .option("y")
            .input(playlist_entry.file)
        )
        message = ''

        if ConversionType.WAV in conversion_type:
            if ConversionType.BIT_24 in conversion_type:
                if ConversionType.DOWNSAMPLE in conversion_type:
                    message = 'Converting to 24-bit 48kHz WAV'
                    ffmpeg = ffmpeg.output(output_location, {"codec:a": "pcm_s24le"}, ar=48000)
                else:
                    message = 'Converting to 24-bit WAV'
                    ffmpeg = ffmpeg.output(output_location, {"codec:a": "pcm_s24le"})
            else:
                if ConversionType.DOWNSAMPLE in conversion_type:
                    message = 'Converting to 48kHz WAV'
                    ffmpeg = ffmpeg.output(output_location, ar=48000)
                else:
                    message = 'Converting to WAV'
                    ffmpeg = ffmpeg.output(output_location)
        elif conversion_type.DOWNSAMPLE in conversion_type:
            ffmpeg = ffmpeg.output(output_location, ar=48000)

        output_location = playlist_entry.transcoded_file(output_root)

        print(f"{message}: {playlist_entry.file}")
        await _run_ffmpeg(ffmpeg, output_location)

    await _tag(playlist_entry.metadata, output_location)
