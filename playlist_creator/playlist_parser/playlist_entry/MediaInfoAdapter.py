import contextlib
import json
import multiprocessing.managers
import os
import subprocess
import sys

from MediaInfo import MediaInfo
from pathvalidate import sanitize_filepath

TAGS_TO_LOAD = [
    'title',
    'artist',
    'display_artist',
    'album_artist',
    'album',
    'track',
    'tracktotal',
    'disc',
    'disctotal',
    'organization',
    'genre',
    'involvedpeople'
]


def get_tag(tags, tag):
    return tags.get(tag) or tags.get(tag.upper())


class MediaInfoAdapter(MediaInfo):
    def __init__(self, lock: multiprocessing.RLock = None, **kwargs):
        super().__init__(**kwargs)

        self._load_metadata_attempted: bool = lock is None
        self._metadata: dict = {}
        self.__lock = lock

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
    def _lock(self):
        return self.__lock if self.__lock else contextlib.nullcontext()

    def contains_metadata(self) -> bool:
        return len(self._get_metadata()) > 0

    def formatted_filename(self) -> str:
        disc = self.disc
        track = self.track
        formatted_track = f"{track or 0:02d}"

        disc_and_track = '-'.join([str(disc), formatted_track]) if disc and track \
            else formatted_track if track \
            else None

        disc_and_track_and_title = ' '.join(info for info in [disc_and_track, self.title] if info)

        filepath = os.sep.join(info for info in
                               [self.album_artist,
                                self.album,
                                disc_and_track_and_title
                                ] if info
                               )

        return sanitize_filepath(
            filepath if sys.platform != 'win32' else filepath.replace(':', ' '),
            replacement_text=' ',
            platform='auto')

    def get(self, key) -> str | None:
        metadata = self._get_metadata()

        if key in metadata:
            return metadata.get(key)

        if self.filename:  # pragma: no cover
            print(
                f"{self.filename}'s metadata does not contain the {key} tag",
                file=sys.stderr,
                flush=True
            )

        return None

    def _get_metadata(self) -> multiprocessing.managers.DictProxy:
        with self._lock:
            if not self._load_metadata_attempted:
                self._load_metadata()

        return self._metadata

    def _load_metadata(self):
        with self._lock:
            if (
                    self._load_metadata_attempted
                    or not os.path.exists(self.filename)
                    # or not os.path.exists(self.cmd)
            ):
                return

            cmd_name = os.path.basename(self.cmd)
            self._load_metadata_attempted = True

            if cmd_name in {'ffprobe', 'ffprobe.exe'}:
                self._metadata.update(self._ffprobe_get_metadata())

    def _ffprobe_get_metadata(self) -> dict:
        ffprobe_output = self._run_ffprobe()
        info_dict = json.loads(ffprobe_output)
        tags = info_dict.get('format').get('tags')
        metadata = {}

        if tags is None:
            print(f"Failed to load metadata for: {self.filename}", file=sys.stderr, flush=True)
        else:
            for tag in TAGS_TO_LOAD:
                metadata[tag] = get_tag(tags, tag)

        return metadata

    def _run_ffprobe(self) -> str:
        return self._try_run(
            f'"{self.cmd}"'
            f' -loglevel quiet -print_format json -show_format -show_error'
            f' -i "{self.filename}"'
        )

    def _try_run(self, cmd) -> str:
        try:
            output_bytes = subprocess.check_output(cmd, shell=True)
        except subprocess.CalledProcessError:
            print(f"Failed to call FFProbe for: {self.filename}", file=sys.stderr, flush=True)
            return ''

        return output_bytes.decode('utf-8')

    def _strip_total(self, key) -> int | None:
        number = self.get(key)
        if number is not None:
            try:
                return int(number.rsplit('/')[0])
            except ValueError:
                print(f"Could not fetch {key} for {self.filename}. Number fetched: {number}")

        return None
