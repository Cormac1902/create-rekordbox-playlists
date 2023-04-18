import os

from Playlist import Playlist
from PlaylistEntry import PlaylistEntry


class PlaylistWriter:
    playlist: Playlist
    playlists_output_directory: str
    transcodes_output_directory: str
    processed_playlist_entries: list[PlaylistEntry]

    def __init__(self, playlist, playlists_output_directory, transcodes_output_directory, processed_playlist_entries):
        self.playlist = playlist
        self.playlists_output_directory = playlists_output_directory
        self.transcodes_output_directory = transcodes_output_directory
        self.processed_playlist_entries = processed_playlist_entries

    def write_playlist(self):
        for playlist_entry in self.processed_playlist_entries:
            if playlist_entry in self.playlist.playlist_entries:
                self.playlist.playlist_entries[playlist_entry].conversion_type = playlist_entry.conversion_type
                self.playlist.playlist_entries[playlist_entry].metadata = playlist_entry.metadata

        playlist_file = os.sep.join([self.playlists_output_directory, f"{self.playlist.title}.pls"])
        print(f"Writing playlist {playlist_file}")

        with open(playlist_file, mode='w', encoding="utf-8") as file:
            file.write('[playlist]\n')
            i = 1

            for playlist_entry in self.playlist.playlist_entries.values():
                file.write(f"File{i}={playlist_entry.file_location(self.transcodes_output_directory)}\n")
                file.write(f"Title{i}={playlist_entry.title}\n")
                file.write(f"Length{i}={playlist_entry.length}\n")
                i = i + 1

            file.write(f"NumberOfEntries={i}")
            file.write('Version=2')
