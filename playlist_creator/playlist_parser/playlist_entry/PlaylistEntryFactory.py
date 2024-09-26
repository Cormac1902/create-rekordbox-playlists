import contextlib
import multiprocessing
import multiprocessing.managers

from playlist_creator import configuration
from .PlaylistEntry import PlaylistEntry
from .PlaylistEntryData import PlaylistEntryData


class PlaylistEntryFactory:
    def __init__(self, config: configuration.Config = None):
        self._config = config
        self._manager = multiprocessing.Manager()
        self._playlist_entries: multiprocessing.managers.DictProxy[
            str, PlaylistEntry] = self._manager.dict()
        self.__lock = self._manager.Lock()

    @property
    def playlist_entries(self):
        return self._playlist_entries

    @property
    def _lock(self):
        return self.__lock if self.__lock else contextlib.nullcontext()

    def add_playlist_entry(self, playlist_entry_data: PlaylistEntryData) -> PlaylistEntry:
        with self._lock:
            if playlist_entry_data not in self._playlist_entries:
                self._playlist_entries[playlist_entry_data.file] = PlaylistEntry(
                    self._manager, playlist_entry_data, self._config
                )

            playlist_entry = self._playlist_entries[playlist_entry_data.file]

        return playlist_entry
