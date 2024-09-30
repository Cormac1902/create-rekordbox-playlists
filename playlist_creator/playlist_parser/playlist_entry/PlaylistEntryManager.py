import multiprocessing.managers

from playlist_creator import audio_file_converter
from .PlaylistEntry import PlaylistEntry


class PlaylistEntryManager(multiprocessing.managers.SyncManager):
    def __init__(self):
        super().__init__()

        #   pylint: disable=no-member
        PlaylistEntryManager.register('PlaylistEntry', PlaylistEntry)
        #   pylint: enable=no-member
