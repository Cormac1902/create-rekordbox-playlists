import os
from typing import List

from PlaylistEntry import PlaylistEntry


class Playlist:
    playlist_entries: List[PlaylistEntry]

    def __init__(self, title, filepath):
        self.title: str = title
        self.filepath: str = filepath
        self.playlist_entries = []

    def write_playlist(self, output_directory, transcodes_output_directory):
        playlist_file = os.sep.join([output_directory, f"{self.title}.pls"])
        print(f"Writing playlist {playlist_file}")

        with open(playlist_file, mode='w', encoding="utf-8") as file:
            file.write('[playlist]\n')
            i = 1

            for playlist_entry in self.playlist_entries:
                file.write(f"File{i}={playlist_entry.file_location(transcodes_output_directory)}\n")
                file.write(f"Title{i}={playlist_entry.title}\n")
                file.write(f"Length{i}={playlist_entry.length}\n")
                i = i + 1

            file.write(f"NumberOfEntries={i}")
            file.write('Version=2')
