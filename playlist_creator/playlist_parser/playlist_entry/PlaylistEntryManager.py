import multiprocessing.managers

from .PlaylistEntry import PlaylistEntry


class PlaylistEntryManager(multiprocessing.managers.SyncManager):
    def __init__(self):
        super().__init__()

        #   pylint: disable=no-member
        PlaylistEntryManager.register('PlaylistEntry', PlaylistEntry)
        #   pylint: enable=no-member
