from .MediaInfoMetadata import MediaInfoMetadata
from pathvalidate import sanitize_filepath

import os
import sys


class PlaylistEntryMetadata:
    media_info_metadata: MediaInfoMetadata
    album_artist: str
    album: str
    track: int
    disc: int
    title: str

    def __init__(self, media_info: MediaInfoMetadata):
        self.media_info_metadata = media_info
        self.album_artist = self.media_info_metadata.get('album_artist')
        self.album = self.media_info_metadata.get('album')
        self.track = self._strip_total('track')
        self.disc = self._strip_total('disc')
        self.title = self.media_info_metadata.get('title')

    def filename(self) -> str:
        filepath = os.sep.join([self.album_artist, self.album,
                                ' '.join(['-'.join([str(self.disc), f"{self.track:02d}"]), self.title])])

        return sanitize_filepath(
            filepath if sys.platform != 'win32' else filepath.replace(':', ' '),
            replacement_text=' ',
            platform='auto')

    def _strip_total(self, key) -> int:
        number = self.media_info_metadata.get(key)
        if number is not None:
            try:
                return int(number.rsplit('/')[0])
            except ValueError:
                print(f"Could not fetch {key} for {self.media_info_metadata.filename}. Number fetched: {number}")

        return 0
