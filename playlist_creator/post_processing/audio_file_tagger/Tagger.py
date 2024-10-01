import taglib

from playlist_creator import audio_file_converter, playlist_parser
from ..PostProcessor import PostProcessor


def _copy_tag(file: taglib.File, tag: str, playlist_entry: playlist_parser.PlaylistEntry,
              make_list=True):
    metadata_tag = playlist_entry.get_metadata_tag(tag)
    if metadata_tag:
        file.tags[tag] = [metadata_tag] if make_list else metadata_tag.split(';')


def _get_tag(playlist_entry: playlist_parser.PlaylistEntry, tag: str, make_list: bool = True):
    metadata_tag = playlist_entry.get_metadata_tag(tag)
    return ([metadata_tag] if make_list else metadata_tag.split(';')) if metadata_tag else None


class Tagger(PostProcessor):
    def __init__(self, successor: PostProcessor = None):
        super().__init__(successor)

    def process(self,
                playlist_entry: playlist_parser.PlaylistEntry,
                transcodes_output_directory: str):
        if (
                playlist_entry.metadata_successfully_loaded()
                and playlist_entry.conversion_type() is not audio_file_converter.ConversionType.NONE
        ):
            output_location = playlist_entry.file_location(transcodes_output_directory)

            tags = {
                key: value for key, value in {
                    tag: _get_tag(playlist_entry, tag, tag not in ['artist', 'genre', 'producer'])
                    for tag in playlist_parser.TAGS_TO_LOAD
                }.items()
                if value
            }

            with taglib.File(output_location, save_on_exit=True) as file:
                if {key.lower(): value for key, value in file.tags.items()} != tags:
                    print(f"Updating tags: {output_location}", flush=True)
                    file.tags = tags
