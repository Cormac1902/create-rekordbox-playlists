import asyncio
import multiprocessing
import os
import re
import sys
import time
from datetime import timedelta
from typing import Optional

import audio_file_converter
import configuration
import playlist_parser
import playlist_writer
import post_processing

_ALLOWED_FORMATS = {'MP3', 'WAV', 'ALAC', 'AIFF'}


def get_playlist(directory, file) -> Optional[playlist_parser.Playlist]:
    filepath = directory + os.sep + file

    return playlist_parser.Playlist(file.removesuffix('.pls'), filepath) if filepath.endswith(
        '.pls') else None


def get_playlists(playlists_path) -> set[playlist_parser.Playlist]:
    directory_playlists = set()

    def add_to_playlists(playlist_path, playlist_file):
        playlist = get_playlist(playlist_path, playlist_file)
        if playlist is not None:
            directory_playlists.add(playlist)

    if os.path.isdir(playlists_path):
        for path, directories, files in os.walk(playlists_path):
            for file in files:
                add_to_playlists(path, file)
    elif os.path.isfile(playlists_path):
        add_to_playlists(os.path.dirname(playlists_path), os.path.basename(playlists_path))

    return directory_playlists


def parse_playlists(
        playlists_to_parse, _playlist_entry_factory: playlist_parser.PlaylistEntryFactory
):
    for playlist in playlists_to_parse:
        with open(playlist.filepath, 'r', encoding='utf-8') as playlist_file:
            playlist_file_lines = playlist_file.readlines()
            line_count = len(playlist_file_lines)
            for i in range(1, line_count - 4, 3):
                file = re.compile(r'File\d+=(.*)').match(playlist_file_lines[i]).group(1)
                title = re.compile(r'Title\d+=(.*)').match(playlist_file_lines[i + 1]).group(1)
                length = re.compile(r'Length\d+=(.*)').match(playlist_file_lines[i + 2]).group(1)
                playlist.playlist_entries.append(
                    _playlist_entry_factory.add_playlist_entry(
                        playlist_parser.PlaylistEntryData(file, title, length)
                    )
                )


def write_playlist(playlist_to_write: playlist_writer.PlaylistWriterContext):
    playlist_to_write.write_playlist()


def get_metadata(playlist_entry: playlist_parser.PlaylistEntry):
    playlist_entry.get_metadata()


def post_process(post_processor: post_processing.PostProcessor,
                 playlist_entry,
                 transcodes_output_directory):
    post_processor.process_chain(playlist_entry, transcodes_output_directory)


def write_playlists(
        playlists_to_write: set[playlist_parser.Playlist],
        _playlist_entry_factory: playlist_parser.PlaylistEntryFactory,
        config: configuration.Config,
        pool: multiprocessing.Pool
):
    playlist_writer_strategy_factory = playlist_writer.PlaylistWriterStrategyFactory()
    playlist_writer_strategy = playlist_writer_strategy_factory.get_writer_strategy(
        playlist_writer.PlsWriterStrategy)

    pool.map_async(
        write_playlist,
        [playlist_writer.PlaylistWriterContext(
            playlist_to_write,
            config.playlists_output_directory,
            config.transcodes_output_directory,
            playlist_writer_strategy
        )
            for playlist_to_write in playlists_to_write
        ]
    )
    pool.map_async(
        get_metadata,
        [playlist_entry
         for playlist_entry
         in _playlist_entry_factory.playlist_entries.values()
         ]
    )


async def convert_files(playlist_entries: set[playlist_parser.PlaylistEntry],
                        converter: audio_file_converter.Converter):
    ffmpeg_tasks = set()

    for playlist_entry in playlist_entries:
        ffmpeg_tasks.add(asyncio.create_task(converter.convert_file(playlist_entry)))

    await asyncio.gather(*ffmpeg_tasks)


def post_process_playlist_entries(playlist_entries: set[playlist_parser.PlaylistEntry],
                                  config: configuration.Config,
                                  pool: multiprocessing.Pool):
    post_processor = post_processing.Tagger(
        post_processing.EnhancedMultichannelAudioFixer()
    )

    pool.starmap(
        post_process, [
            (post_processor, playlist_entry, config.transcodes_output_directory)
            for playlist_entry in playlist_entries
        ]
    )


async def main(config: configuration.Config):
    playlists = get_playlists(config.playlists_directory)

    with playlist_parser.PlaylistEntryManager() as manager:
        playlist_entry_factory = playlist_parser.PlaylistEntryFactory(config, manager)

        parse_playlists(playlists, playlist_entry_factory)

        with multiprocessing.Pool(config.max_parallel_tasks) as pool:
            write_playlists(playlists, playlist_entry_factory, config, pool)

            processed_files = playlist_entry_factory.playlist_entries.values()

            await convert_files(
                processed_files,
                audio_file_converter.Converter(config.max_parallel_tasks ^ 2,
                                               config.transcodes_output_directory)
            )

            post_process_playlist_entries(processed_files, config, pool)


if __name__ == '__main__':
    started_at = time.time()

    max_parallel_tasks = os.cpu_count()

    if len(sys.argv) > 4:
        max_parallel_tasks_argv = int(sys.argv[4])
        if max_parallel_tasks_argv > 0:
            max_parallel_tasks = max_parallel_tasks_argv

    config_argv = configuration.Config(
        _ALLOWED_FORMATS, sys.argv[1], sys.argv[2], sys.argv[3], max_parallel_tasks
    )

    asyncio.run(main(config_argv))

    finished_at = time.time()
    elapsed_time = finished_at - started_at
    print(f"Done in {timedelta(seconds=elapsed_time)}")
