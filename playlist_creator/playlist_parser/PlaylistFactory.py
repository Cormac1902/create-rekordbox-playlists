import contextlib
import os
import threading

from .Playlist import Playlist

class PlaylistFactory:
    def __init__(self, lock: threading.Lock = None):
        self._playlists: dict[str, Playlist] = {}
        self.__lock = lock

    @property
    def playlists(self) -> set[Playlist]:
        return set(self._playlists.values())

    @property
    def _lock(self):
        return self.__lock if self.__lock else contextlib.nullcontext()

    def add_playlist(self, directory, file, playlists_path = None):
        if not file.endswith('.pls'):
            return

        filepath = os.path.join(directory, file)
        title = file.removesuffix('.pls')

        with self._lock:
            if title not in self._playlists:
                self._playlists[title] = Playlist(
                    title,
                    str(filepath),
                    str(os.path.relpath(directory, playlists_path)) if playlists_path else None
                )
