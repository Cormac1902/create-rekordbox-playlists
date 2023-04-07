import asyncio
import os
import re
import sys

import soundfile

import Converter

from ConversionTypeEnum import ConversionType
from MediaInfoMetadata import MediaInfoMetadata
from Playlist import Playlist
from PlaylistEntry import PlaylistEntry
from PlaylistEntryMetadata import PlaylistEntryMetadata

_ALLOWED_FORMATS = {'MP3', 'WAV', 'ALAC', 'AIFF'}


def get_playlists(directory):
    directory_playlists = []
    assert os.path.isdir(directory)
    for path, directories, files in os.walk(directory):
        for file in files:
            filepath = path + os.sep + file

            if filepath.endswith('.pls'):
                directory_playlists.append(Playlist(file.removesuffix('.pls'), filepath))

    return directory_playlists


def parse_playlists(playlists_to_parse):
    for playlist in playlists_to_parse:
        playlist_file = open(playlist.filepath, 'r', encoding='utf-8')
        playlist_file_lines = playlist_file.readlines()
        line_count = len(playlist_file_lines)
        for i in range(1, line_count - 4, 3):
            file = re.compile(r'File\d+=(.*)').match(playlist_file_lines[i]).group(1)
            title = re.compile(r'Title\d+=(.*)').match(playlist_file_lines[i + 1]).group(1)
            length = re.compile(r'Length\d+=(.*)').match(playlist_file_lines[i + 2]).group(1)
            playlist.playlist_entries.append(PlaylistEntry(file, title, length))


if __name__ == '__main__':
    playlists = get_playlists(sys.argv[1])
    output_directory = sys.argv[2]
    parse_playlists(playlists)

    for parsed_playlist in playlists:
        for playlist_entry in parsed_playlist.playlist_entries:
            playlist_entry_soundfile = soundfile.SoundFile(playlist_entry.file)
            mediainfo = MediaInfoMetadata(
                filename=playlist_entry.file, cmd=r'C:\Program Files\ffmpeg\ffprobe.exe'
            )
            playlist_entry.metadata = PlaylistEntryMetadata(mediainfo)
            if playlist_entry_soundfile.format not in _ALLOWED_FORMATS:
                playlist_entry.add_conversion_type(ConversionType.WAV)
            if playlist_entry_soundfile.samplerate > 48000:
                playlist_entry.add_conversion_type(ConversionType.DOWNSAMPLE)
            if playlist_entry_soundfile.subtype == 'PCM_24':
                playlist_entry.add_conversion_type(ConversionType.BIT_24)

            asyncio.run(Converter.convert(playlist_entry, output_directory))
