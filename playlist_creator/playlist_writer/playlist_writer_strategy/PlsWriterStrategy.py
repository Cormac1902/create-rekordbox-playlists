import logging
import os
import pathlib

from playlist_creator import playlist_parser
from .PlaylistWriterStrategy import PlaylistWriterStrategy

logger = logging.getLogger(__name__)


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
        logger.info(f"Writing playlist {playlist_file}")

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

            number_of_entries = i - 1

            file.writelines([
                f"NumberOfEntries={number_of_entries}\n",
                'Version=2'
            ])

            logger.info(f"Wrote playlist {playlist_file}")

            if len(playlist.playlist_entries) > number_of_entries:
                logger.warning(f"Missing entries from {playlist_file}. "
                               f"{playlist.title}: {len(playlist.playlist_entries)}; "
                               f"{playlist_file}: {number_of_entries}")

    def __hash__(self):
        return hash('pls')
