import contextlib
import multiprocessing
import os
import sys
from abc import abstractmethod

from pathvalidate import sanitize_filepath

from . import media_info_strategy


class MetadataAdapter:
    def __init__(self,
                 strategy: media_info_strategy.IMediaInfoStrategy = None,
                 filename: str = None,
                 lock: multiprocessing.RLock = None):
        self._filename = filename
        self._metadata: dict = {}
        self._strategy = strategy
        self.__lock = lock
        self._load_metadata_attempted: bool = self.__lock is None

    @property
    @abstractmethod
    def album(self) -> str:
        return self.get('album')

    @property
    @abstractmethod
    def album_artist(self) -> str:
        return self.get('album_artist')

    @property
    @abstractmethod
    def disc(self) -> int | None:
        return self._strip_total('disc')

    @property
    @abstractmethod
    def title(self) -> str:
        return self.get('title')

    @property
    @abstractmethod
    def track(self) -> int | None:
        return self._strip_total('track')

    @property
    def contains_metadata(self) -> bool:
        return len(self._get_metadata()) > 0

    @property
    def _lock(self):
        return self.__lock if self.__lock else contextlib.nullcontext()

    def formatted_filename(self) -> str:
        disc = self.disc
        track = self.track
        formatted_track = f"{track or 0:02d}"

        disc_and_track = '-'.join([str(disc), formatted_track]) if disc and track \
            else formatted_track if track \
            else None

        disc_and_track_and_title = ' '.join(
            info for info in [disc_and_track, self.title] if info)

        filepath = os.sep.join(info for info in
                               [self.album_artist,
                                self.album,
                                disc_and_track_and_title
                                ] if info
                               )

        return sanitize_filepath(
            filepath if sys.platform != 'win32' else filepath.replace(':', ' '),
            replacement_text=' ',
            platform='auto'
        ) if filepath else ''

    def get(self, key) -> str | None:
        metadata = self._get_metadata()

        if key in metadata:
            return metadata.get(key)

        if self._filename:  # pragma: no cover
            print(
                f"{self._filename}'s metadata does not contain the {key} tag",
                file=sys.stderr,
                flush=True
            )

        return None

    def _get_metadata(self) -> dict:
        with self._lock:
            if not self._load_metadata_attempted:
                self._load_metadata()

            return self._metadata

    def _load_metadata(self):
        with self._lock:
            if self._load_metadata_attempted:
                return

            self._load_metadata_attempted = True

            self._metadata.update(self._strategy.get_metadata(self._filename))

    def _strip_total(self, key) -> int | None:
        number = self.get(key)
        if number is not None:
            try:
                return int(number.rsplit('/')[0])
            except ValueError:
                print(
                    f"Could not fetch {key} for {self._filename}. Number fetched: {number}",
                    file=sys.stderr,
                    flush=True
                )

        return None
