import asyncio
import multiprocessing
import os
import re
import sys
import time
from datetime import timedelta

from Config import Config
from Converter import Converter
from Playlist import Playlist
from PlaylistEntry import PlaylistEntry
from PlaylistWriter import PlaylistWriter
from Tagger import Tagger

_ALLOWED_FORMATS = {'MP3', 'WAV', 'ALAC', 'AIFF'}


def get_playlists(directory) -> set[Playlist]:
    directory_playlists = set()
    assert os.path.isdir(directory)
    for path, directories, files in os.walk(directory):
        for file in files:
            filepath = path + os.sep + file

            if filepath.endswith('.pls'):
                directory_playlists.add(Playlist(file.removesuffix('.pls'), filepath))

    return directory_playlists


def parse_playlists(playlists_to_parse):
    for playlist in playlists_to_parse:
        with open(playlist.filepath, 'r', encoding='utf-8') as playlist_file:
            playlist_file_lines = playlist_file.readlines()
            line_count = len(playlist_file_lines)
            for i in range(1, line_count - 4, 3):
                file = re.compile(r'File\d+=(.*)').match(playlist_file_lines[i]).group(1)
                title = re.compile(r'Title\d+=(.*)').match(playlist_file_lines[i + 1]).group(1)
                length = re.compile(r'Length\d+=(.*)').match(playlist_file_lines[i + 2]).group(1)
                playlist_entry = PlaylistEntry(file, title, length)
                playlist.playlist_entries[playlist_entry] = playlist_entry


def determine_conversion_type(playlist_entry: PlaylistEntry):
    playlist_entry.determine_conversion_type(_ALLOWED_FORMATS)
    return playlist_entry


def tag(tagger: Tagger):
    tagger.tag()


def determine_conversion_types(parsed_playlists: set[Playlist], config: Config) -> list[PlaylistEntry]:
    processed_files_to_return = dict()

    for parsed_playlist in parsed_playlists:
        print(f"Processing {parsed_playlist.title}")
        for playlist_entry in parsed_playlist.playlist_entries:
            if playlist_entry in processed_files_to_return:
                print(f"Already processed: {playlist_entry.file}")
            else:
                processed_files_to_return[playlist_entry] = playlist_entry

    print(f"Found {len(processed_files_to_return)} unique files")

    with multiprocessing.Pool(config.max_parallel_tasks) as pool:
        return pool.map(determine_conversion_type, processed_files_to_return)


def write_playlist(playlist_to_write: PlaylistWriter):
    playlist_to_write.write_playlist()


def write_playlists(playlists_to_write: set[Playlist], processed_playlist_entries: list[PlaylistEntry], config: Config):
    with multiprocessing.Pool(config.max_parallel_tasks) as pool:
        pool.map(write_playlist,
                 [PlaylistWriter(playlist_to_write,
                                 config.playlists_output_directory,
                                 config.transcodes_output_directory,
                                 processed_playlist_entries)
                  for playlist_to_write in playlists_to_write]
                 )


async def convert_files(playlist_entries: list[PlaylistEntry], converter: Converter):
    ffmpeg_tasks = set()

    for playlist_entry in playlist_entries:
        ffmpeg_tasks.add(asyncio.create_task(converter.convert_file(playlist_entry)))

    await asyncio.gather(*ffmpeg_tasks)


def update_tags(playlist_entries: list[PlaylistEntry], config: Config):
    with multiprocessing.Pool(config.max_parallel_tasks) as pool:
        pool.map(
            tag, [Tagger(playlist_entry, config.transcodes_output_directory) for playlist_entry in playlist_entries]
        )


if __name__ == '__main__':
    started_at = time.time()

    max_parallel_tasks = os.cpu_count()

    if len(sys.argv) > 4:
        max_parallel_tasks_argv = int(sys.argv[4])
        if max_parallel_tasks_argv > 0:
            max_parallel_tasks = max_parallel_tasks_argv

    config_argv = Config(sys.argv[1], sys.argv[2], sys.argv[3], max_parallel_tasks)

    playlists = get_playlists(config_argv.playlists_directory)

    parse_playlists(playlists)

    processed_files = determine_conversion_types(playlists, config_argv)

    write_playlists(playlists, processed_files, config_argv)

    asyncio.run(
        convert_files(
            processed_files, Converter(config_argv.max_parallel_tasks, config_argv.transcodes_output_directory)
        )
    )

    update_tags(processed_files, config_argv)

    finished_at = time.time()
    elapsed_time = finished_at - started_at
    print(f"Done in {timedelta(seconds=elapsed_time)}")
