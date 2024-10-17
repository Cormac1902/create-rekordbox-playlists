import asyncio
import concurrent.futures
import datetime
import itertools
import multiprocessing
import os
import re
import sys
import threading
import time

import audio_file_converter
import configuration
import playlist_parser
import playlist_writer
import post_processing

_ALLOWED_FORMATS = {'MP3', 'WAV', 'ALAC', 'AIFF'}


def get_playlists(playlists_path, playlist_factory: playlist_parser.PlaylistFactory):
    if os.path.isdir(playlists_path):
        [
            [playlist_factory.add_playlist(path, file, playlists_path) for file in files]
            for path, directories, files in os.walk(playlists_path)
        ]
    elif os.path.isfile(playlists_path):
        playlist_factory.add_playlist(
            os.path.dirname(playlists_path), os.path.basename(playlists_path)
        )


def parse_playlist(
        playlist: playlist_parser.Playlist,
        _playlist_entry_factory: playlist_parser.PlaylistEntryFactory
):
    print(f"Parsing {playlist.title_and_path}")

    file_regex = re.compile(r'File\d+=(.*)')
    title_regex = re.compile(r'Title\d+=(.*)')
    length_regex = re.compile(r'Length\d+=(.*)')

    with open(playlist.filepath, 'r', encoding='utf-8') as playlist_file:
        playlist_file.readline()
        while (len(
                next_playlist_entry := [
                    line.strip() for line in itertools.islice(playlist_file, 3)
                ]
        )) > 2:
            file = file_regex.match(next_playlist_entry[0]).group(1)
            title = title_regex.match(next_playlist_entry[1]).group(1)
            length = length_regex.match(next_playlist_entry[2]).group(1)
            playlist.playlist_entries.append(
                _playlist_entry_factory.add_playlist_entry(
                    playlist_parser.PlaylistEntryData(file, title, length)
                )
            )

        print(f"Parsed {playlist.title_and_path}")


def parse_playlists(
        playlist_factory: playlist_parser.PlaylistFactory,
        _playlist_entry_factory: playlist_parser.PlaylistEntryFactory,
        executor: concurrent.futures.ThreadPoolExecutor
):
    [
        executor.submit(
            parse_playlist, playlist, _playlist_entry_factory
        ) for playlist in playlist_factory.playlists
    ]


def write_playlist(playlist_to_write: playlist_writer.PlaylistWriterContext):
    playlist_to_write.write_playlist()


def get_metadata(playlist_entry: playlist_parser.PlaylistEntry):
    playlist_entry.get_metadata()

    return playlist_entry


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
    return pool.map_async(get_metadata, list(_playlist_entry_factory.playlist_entries.values()))


async def convert_files(playlist_entries: set[playlist_parser.PlaylistEntry],
                        converter: audio_file_converter.Converter):


    async with asyncio.TaskGroup() as task_group:
        [
            task_group.create_task(
                converter.convert_file(audio_file_converter.ConverterContext(playlist_entry))
            )
            for playlist_entry
            in playlist_entries
        ]


def post_process_playlist_entries(playlist_entries: set[playlist_parser.PlaylistEntry],
                                  config: configuration.Config,
                                  pool: multiprocessing.Pool,
                                  add_asynchronously=False):
    post_processor = post_processing.Tagger(
        post_processing.EnhancedMultichannelAudioFixer()
    )

    tasks = [
        (post_processor, playlist_entry, config.transcodes_output_directory)
        for playlist_entry
        in playlist_entries
    ]

    pool.starmap_async(
        post_process, tasks
    ) if add_asynchronously else pool.starmap(
        post_process, tasks
    )


async def main(config: configuration.Config):
    playlist_factory = playlist_parser.PlaylistFactory(threading.Lock())

    get_playlists(config.playlists_directory, playlist_factory)

    with playlist_parser.PlaylistEntryManager() as manager:
        playlist_entry_factory = playlist_parser.PlaylistEntryFactory(config, manager)

        with concurrent.futures.ThreadPoolExecutor(config.max_parallel_tasks) as executor:
            parse_playlists(playlist_factory, playlist_entry_factory, executor)

        with multiprocessing.Pool(config.max_parallel_tasks) as pool:
            playlist_entries = write_playlists(
                playlist_factory.playlists, playlist_entry_factory, config, pool
            )

            files_to_post_process, files_to_convert = set(), set()
            [
                (
                    files_to_post_process
                    if playlist_entry.transcoded_file_exists(config.transcodes_output_directory)
                    else files_to_convert
                ).add(playlist_entry)
                for playlist_entry
                in playlist_entries.get()
                if not playlist_entry.conversion_type_is_none()
            ]

            post_process_playlist_entries(
                files_to_post_process,
                config,
                pool,
                len(files_to_convert) > 0
            )

            converter_strategy_factory = audio_file_converter.ConverterStrategyFactory()
            converter_factory = audio_file_converter.ConverterFactory(asyncio.Lock())

            await convert_files(
                files_to_convert,
                audio_file_converter.Converter(
                    asyncio.Semaphore(config.max_parallel_tasks),
                    config.transcodes_output_directory,
                    converter_strategy_factory.get_strategy(
                        audio_file_converter.WAVStrategy,
                        converter_factory=converter_factory
                    )
                )
            )

            post_process_playlist_entries(files_to_convert, config, pool)


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
    print(f"Done in {datetime.timedelta(seconds=elapsed_time)}")
