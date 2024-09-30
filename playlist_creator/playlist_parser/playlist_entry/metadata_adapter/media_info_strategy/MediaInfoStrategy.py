import json

from .IMediaInfoStrategy import IMediaInfoStrategy, get_tag

MEDIA_INFO_STRATEGY_FORMATS = {
    'OGG'
}
_TAGS_MAPPING = {
    'title': 'Track',
    'artist': 'Performer',
    'album_artist': 'Album_Performer',
    'track': 'Track_Position',
    'tracktotal': 'Track_Position_Total',
    'disc': 'Part',
    'disctotal': 'Part_Position_Total',
    'organization': 'Producer'
}


#   pylint: disable=too-few-public-methods


class MediaInfoStrategy(IMediaInfoStrategy):
    def __init__(self, cmd='mediainfo', **kwargs):
        super().__init__(cmd, **kwargs)

    def _get_cmd(self, filename):
        return f'"{self._cmd}" --Output=JSON "{filename}"'

    def _get_metadata_from_cmd(self, cmd_output: str) -> dict:
        return json.loads(cmd_output).get('media').get('track')[0]

    def _get_tag(self, tags, tag):
        return get_tag(
            tags | tags['extra'], _TAGS_MAPPING[tag] if tag in _TAGS_MAPPING else tag.title()
        )

#   pylint: enable=too-few-public-methods
