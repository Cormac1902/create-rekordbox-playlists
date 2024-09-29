import subprocess
import sys
from abc import ABC, abstractmethod


def get_tag(tags, tag):
    return tags.get(tag) or tags.get(tag.upper())


def try_run(cmd) -> str:
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

    @abstractmethod
    def get_metadata(self, filename: str) -> dict:
        pass

    def __hash__(self):
        return hash(self._cmd)

#   pylint: enable=too-few-public-methods
