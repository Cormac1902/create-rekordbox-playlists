import json

from .IMediaInfoStrategy import IMediaInfoStrategy


#   pylint: disable=too-few-public-methods

class FfprobeStrategy(IMediaInfoStrategy):
    def __init__(self, cmd='ffprobe', **kwargs):
        super().__init__(cmd, **kwargs)

    def _get_cmd(self, filename):
        return (f'"{self._cmd}"'
                f' -loglevel quiet -print_format json -show_format -show_error'
                f' -i "{filename}"')

    def _get_metadata_from_cmd(self, cmd_output: str) -> dict:
        return json.loads(cmd_output).get('format').get('tags')

#   pylint: enable=too-few-public-methods
