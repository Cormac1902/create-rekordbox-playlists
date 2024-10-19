import contextlib
import logging
import multiprocessing
import os
import sys

from pathvalidate import sanitize_filepath

from . import media_info_strategy

logger = logging.getLogger(__name__)


class MetadataAdapter:
    def __init__(self,
                 strategy: media_info_strategy.IMediaInfoStrategy = None,
                 filename: str = None,
                 lock: multiprocessing.Lock = None):
        self._filename = filename
        self._metadata: dict = {}
        self._strategy = strategy
        self.__lock = lock
        self._load_metadata_attempted: bool = self.__lock is None

    @property
    def album(self) -> str:
        return self.get('album')

    @property
    def album_artist(self) -> str:
        return self.get('album_artist')

    @property
    def disc(self) -> int | None:
        return self._strip_total('disc')

    @property
    def title(self) -> str:
        return self.get('title')

    @property
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

        def strip_slashes(string: str) -> str:
            return (string
                    .replace(os.sep, ' ')
                    .replace('\\', ' ')
                    .replace('/', ' ')
                    ) if string else str()

        disc_and_track = '-'.join([str(disc), formatted_track]) if disc and track \
            else formatted_track if track \
            else None

        disc_and_track_and_title = ' '.join(
            info for info in [disc_and_track, strip_slashes(self.title)] if info)

        filepath = os.sep.join(info for info in
                               [strip_slashes(self.album_artist),
                                strip_slashes(self.album),
                                disc_and_track_and_title
                                ] if info
                               )

        return sanitize_filepath(
            filepath if sys.platform != 'win32' else filepath.replace(':', ' '),
            replacement_text=' ',
            platform='auto'
        ) if filepath else ''

    def get(self, key) -> str | None:
        if not self.contains_metadata:
            return None

        metadata = self._get_metadata()

        if key in metadata:
            return metadata.get(key)

        logger.warning(f"{self._filename}'s metadata does not contain the {key} tag")

        return None

    def load_metadata(self):
        with self._lock:
            if self._load_metadata_attempted:
                return

            self._metadata.update(self._strategy.get_metadata(self._filename))

            self._load_metadata_attempted = True

    def _get_metadata(self) -> dict:
        if not self._load_metadata_attempted:
            self.load_metadata()

        return self._metadata

    def _strip_total(self, key) -> int | None:
        number = self.get(key)
        if number is not None:
            try:
                return int(number.rsplit('/')[0]) or int(number)
            except ValueError:
                logger.warning(
                    f"Could not fetch {key} for {self._filename}. Number fetched: {number}"
                )

        return None
