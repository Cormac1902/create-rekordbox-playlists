import json
import os
import shutil
import sys

from .IMediaInfoStrategy import IMediaInfoStrategy, get_tag, try_run

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


#   pylint: disable=too-few-public-methods

class FfprobeStrategy(IMediaInfoStrategy):
    def __init__(self, cmd='ffprobe', **kwargs):
        super().__init__(cmd, **kwargs)

    def get_metadata(self, filename: str) -> dict:
        if not os.path.exists(filename):
            return {}

        ffprobe_output = self._run_ffprobe(filename)
        info_dict = json.loads(ffprobe_output)
        tags = info_dict.get('format').get('tags')
        metadata = {}

        if tags is None:
            print(f"Failed to load metadata for: {filename}", file=sys.stderr, flush=True)
        else:
            for tag in TAGS_TO_LOAD:
                metadata[tag] = get_tag(tags, tag)

        return metadata

    def _run_ffprobe(self, filename) -> str:
        if not shutil.which(self._cmd):
            return ''

        return try_run(
            f'"{self._cmd}"'
            f' -loglevel quiet -print_format json -show_format -show_error'
            f' -i "{filename}"'
        )

#   pylint: enable=too-few-public-methods
