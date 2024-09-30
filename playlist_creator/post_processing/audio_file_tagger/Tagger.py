import taglib

from playlist_creator import audio_file_converter, playlist_parser
from ..PostProcessor import PostProcessor


def _copy_tag(file: taglib.File, tag: str, playlist_entry: playlist_parser.PlaylistEntry,
              make_list=True):
    metadata_tag = playlist_entry.get_metadata_tag(tag)
    if metadata_tag:
        file.tags[tag] = [metadata_tag] if make_list else metadata_tag.split(';')


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
            print(f"Updating tags: {output_location}", flush=True)
            with taglib.File(output_location, save_on_exit=True) as file:
                file.tags = dict()
                for tag in playlist_parser.TAGS_TO_LOAD:
                    _copy_tag(file,
                              tag,
                              playlist_entry,
                              tag not in ['artist', 'genre', 'producer'])
