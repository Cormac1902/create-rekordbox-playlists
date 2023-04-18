import os
import sys

from pathvalidate import sanitize_filepath

from MediaInfoMetadata import MediaInfoMetadata


class PlaylistEntryMetadata:
    raw_metadata: MediaInfoMetadata
    album_artist: str
    album: str
    track: int
    disc: int
    title: str

    def __init__(self, media_info: MediaInfoMetadata):
        self.raw_metadata = media_info.get_metadata()
        self.album_artist = self.raw_metadata.get('album_artist')
        self.album = self.raw_metadata.get('album')
        self.track = self._strip_total('track')
        self.disc = self._strip_total('disc')
        self.title = self.raw_metadata.get('title')

    def filename(self) -> str:
        filepath = os.sep.join([self.album_artist, self.album,
                                ' '.join(['-'.join([str(self.disc), f"{self.track:02d}"]), self.title])])

        return sanitize_filepath(
            filepath if sys.platform != 'win32' else filepath.replace(':', ' '),
            replacement_text=' ',
            platform='auto')

    def _strip_total(self, key) -> int:
        number = self.raw_metadata.get(key)
        if number is not None:
            return int(number.rsplit('/')[0])

        return 0
