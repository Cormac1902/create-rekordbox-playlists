from .MediaInfoAdapter import MediaInfoAdapter
from pathvalidate import sanitize_filepath

import os
import sys


class PlaylistEntryMetadata:
    media_info_metadata: MediaInfoAdapter
    _album: str
    _album_artist: str
    _disc: int | None
    _title: str
    _track: int | None

    def __init__(self,
                 media_info: MediaInfoAdapter = MediaInfoAdapter(),
                 album: str = None,
                 album_artist: str = None,
                 disc: int = None,
                 title: str = None,
                 track: int = None):
        self.media_info_metadata = media_info
        self._album = album
        self._album_artist = album_artist
        self._disc = disc
        self._title = title
        self._track = track

    def get_album_artist(self):
        if self._album_artist is None:
            self._album_artist = self.media_info_metadata.get('album_artist')

        return self._album_artist

    def get_album(self):
        if self._album is None:
            self._album = self.media_info_metadata.get('album')

        return self._album

    def get_disc(self):
        if self._disc is None:
            self._disc = self._strip_total('disc')

        return self._disc

    def get_title(self):
        if self._title is None:
            self._title = self.media_info_metadata.get('title')

        return self._title

    def get_track(self):
        if self._track is None:
            self._track = self._strip_total('track')

        return self._track

    def contains_metadata(self) -> bool:
        return self.media_info_metadata.contains_metadata()

    def filename(self) -> str:
        disc = self.get_disc()
        track = self.get_track()
        formatted_track = f"{track or 0:02d}"

        disc_and_track = '-'.join([str(disc), formatted_track]) if disc and track \
            else formatted_track if track \
            else None

        disc_and_track_and_title = ' '.join(info for info in [disc_and_track, self.get_title()] if info)

        filepath = os.sep.join(info for info in
            [self.get_album_artist(),
             self.get_album(),
             disc_and_track_and_title
             ] if info
        )

        return sanitize_filepath(
            filepath if sys.platform != 'win32' else filepath.replace(':', ' '),
            replacement_text=' ',
            platform='auto')

    def _strip_total(self, key) -> int | None:
        number = self.media_info_metadata.get(key)
        if number is not None:
            try:
                return int(number.rsplit('/')[0])
            except ValueError:
                print(f"Could not fetch {key} for {self.media_info_metadata.filename}. Number fetched: {number}")

        return None
