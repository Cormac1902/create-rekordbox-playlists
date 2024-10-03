import os
import pathlib

from playlist_creator import playlist_parser
from .PlaylistWriterStrategy import PlaylistWriterStrategy


class PlsWriterStrategy(PlaylistWriterStrategy):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def write_playlist(self,
                       playlist: playlist_parser.Playlist,
                       playlists_output_directory: str,
                       transcodes_output_directory: str):
        if playlist.path_from_playlists_directory:
            pathlib.Path(
                os.path.join(playlists_output_directory, playlist.path_from_playlists_directory)
            ).mkdir(parents=True, exist_ok=True)
        playlist_file = os.path.join(playlists_output_directory, f"{playlist.title_and_path}.pls")
        print(f"Writing playlist {playlist_file}")

        with open(playlist_file, mode='w', encoding="utf-8") as file:
            file.write('[playlist]\n')
            i = 1

            for playlist_entry in playlist.playlist_entries:
                if playlist_entry.metadata_successfully_loaded():
                    file.writelines([
                        f"File{i}={playlist_entry.file_location(transcodes_output_directory)}\n",
                        f"Title{i}={playlist_entry.title()}\n",
                        f"Length{i}={playlist_entry.length()}\n"
                    ])
                    i = i + 1

            file.writelines([
                f"NumberOfEntries={i - 1}\n",
                'Version=2'
            ])

    def __hash__(self):
        return hash('pls')
