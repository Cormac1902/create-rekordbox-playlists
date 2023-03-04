import os
import re
import sys

from Playlist import Playlist
from PlaylistEntry import PlaylistEntry


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
        playlist_file = open(playlist.filepath, 'r')
        playlist_file_lines = playlist_file.readlines()
        line_count = len(playlist_file_lines)
        for i in range(1, line_count - 2, 3):
            file = re.compile(r'File\d+=(.*)').match(playlist_file_lines[i]).group(1)
            title = re.compile(r'Title\d+=(.*)').match(playlist_file_lines[i + 1]).group(1)
            length = re.compile(r'Length\d+=(.*)').match(playlist_file_lines[i + 2]).group(1)
            playlist.playlist_entries.append(PlaylistEntry(file, title, length))


if __name__ == '__main__':
    print(sys.argv)
    playlists = get_playlists(sys.argv[1])
    parse_playlists(playlists)
    for parsed_playlist in playlists:
        print(parsed_playlist.filepath)
        print(parsed_playlist.title)
        for playlist_entry in parsed_playlist.playlist_entries:
            print(playlist_entry.file)
            print(playlist_entry.title)
            print(playlist_entry.length)
