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
    metadata = dict()

    def get(self, key) -> str:
        if key in self.metadata:
            return self.metadata.get(key)

        print(f"{self.filename}'s metadata does not contain the {key} tag", file=sys.stderr, flush=True)
        return ''

    def get_metadata(self):
        if not os.path.exists(self.filename) or not os.path.exists(self.cmd):
            return None

        cmd_name = os.path.basename(self.cmd)

        if cmd_name == 'ffprobe' or 'ffprobe.exe':
            self._ffprobe_get_metadata()

        return self.metadata

    def _ffprobe_get_metadata(self):
        ffprobe_output = self._run_ffprobe()
        info_dict = json.loads(ffprobe_output)

        tags = info_dict.get('format').get('tags')

        if tags is None:
            print(f"Failed to load metadata for: {self.filename}", file=sys.stderr, flush=True)
            return

        for tag in TAGS_TO_LOAD:
            self.metadata[tag] = get_tag(tags, tag)

    def _run_ffprobe(self) -> str:
        return _try_run(
            f'"{self.cmd}" -loglevel quiet -print_format json -show_format -show_error -i "{self.filename}"'
        )
