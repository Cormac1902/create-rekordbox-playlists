import json
import os
import subprocess
import sys

from MediaInfo import MediaInfo

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


def _try_run(cmd) -> str:
    try:
        output_bytes = subprocess.check_output(cmd, shell=True)
    except subprocess.CalledProcessError:
        return ''

    return output_bytes.decode('utf-8')


class MediaInfoMetadata(MediaInfo):
    _metadata: dict

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._metadata = dict()
        self._load_metadata()

    def contains_metadata(self) -> bool:
        return len(self._metadata) > 0

    def get(self, key) -> str:
        if key in self._metadata:
            return self._metadata.get(key)

        print(f"{self.filename}'s metadata does not contain the {key} tag", file=sys.stderr, flush=True)
        return ''

    def _load_metadata(self):
        if not os.path.exists(self.filename) or not os.path.exists(self.cmd):
            return None

        cmd_name = os.path.basename(self.cmd)

        if cmd_name == 'ffprobe' or 'ffprobe.exe':
            self._metadata = self._ffprobe_get_metadata()

    def _ffprobe_get_metadata(self) -> dict:
        ffprobe_output = self._run_ffprobe()
        info_dict = json.loads(ffprobe_output)
        tags = info_dict.get('format').get('tags')
        metadata = dict()

        if tags is None:
            print(f"Failed to load metadata for: {self.filename}", file=sys.stderr, flush=True)
        else:
            for tag in TAGS_TO_LOAD:
                metadata[tag] = get_tag(tags, tag)

        return metadata

    def _run_ffprobe(self) -> str:
        return _try_run(
            f'"{self.cmd}" -loglevel quiet -print_format json -show_format -show_error -i "{self.filename}"'
        )
