import contextlib
import multiprocessing

from playlist_creator import configuration
from .PlaylistEntry import PlaylistEntry
from .PlaylistEntryData import PlaylistEntryData
from .PlaylistEntryLocks import PlaylistEntryLocks
from .PlaylistEntryManager import PlaylistEntryManager


class PlaylistEntryFactory:
    __lock: multiprocessing.Lock = None

    def __init__(self,
                 config: configuration.Config = None,
                 manager: PlaylistEntryManager = None):
        self._config = config
        self._manager = manager
        self._playlist_entries = {}

        if self._manager:
            self._playlist_entries = self._manager.dict()
            self.__lock = self._manager.Lock()

    @property
    def playlist_entries(self):
        return self._playlist_entries

    @property
    def _lock(self):
        return self.__lock if self.__lock else contextlib.nullcontext()

    def add_playlist_entry(self, playlist_entry_data: PlaylistEntryData) -> PlaylistEntry:
        with self._lock:
            if playlist_entry_data.file not in self._playlist_entries:
                self._playlist_entries[playlist_entry_data.file] = self._manager.PlaylistEntry(
                    PlaylistEntryLocks(
                        self._manager.Lock(), self._manager.Lock(), self._manager.dict()),
                    playlist_entry_data,
                    self._config
                )

            playlist_entry = self._playlist_entries[playlist_entry_data.file]

        return playlist_entry
