import multiprocessing.managers

from .PlaylistEntry import PlaylistEntry


class PlaylistEntryManager(multiprocessing.managers.SyncManager):
    def __init__(self):
        super().__init__()

        PlaylistEntryManager.register('PlaylistEntry', PlaylistEntry)
