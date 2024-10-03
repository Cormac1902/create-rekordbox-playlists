import os
import shutil
import subprocess
import sys
from abc import ABC, abstractmethod

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
        print(f"Failed to call {cmd}", file=sys.stderr, flush=True)
        return ''

    return output_bytes.decode('utf-8')


#   pylint: disable=too-few-public-methods

class IMediaInfoStrategy(ABC):
    def __init__(self, cmd, **kwargs):
        super().__init__(**kwargs)
        self._cmd = cmd

    def get_metadata(self, filename: str) -> dict:
        if not os.path.exists(filename):
            return {}

        cmd_output = self._run_cmd(filename)
        tags = self._get_metadata_from_cmd(cmd_output)

        if tags is None:  # pragma: no cover
            if filename:
                print(f"Failed to load metadata for: {filename}", file=sys.stderr, flush=True)
        else:
            return {tag: self._get_tag(tags, tag) for tag in TAGS_TO_LOAD}

        return {}

    @abstractmethod
    def _get_cmd(self, filename):
        pass

    @abstractmethod
    def _get_metadata_from_cmd(self, cmd_output: str) -> dict:
        pass

    def _get_tag(self, tags, tag):
        return get_tag(tags, tag)

    def _run_cmd(self, filename: str) -> str:
        if not shutil.which(self._cmd):
            return ''

        return _try_run(self._get_cmd(filename))

    def __hash__(self):
        return hash(self._cmd)

#   pylint: enable=too-few-public-methods
