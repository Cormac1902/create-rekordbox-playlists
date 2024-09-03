from playlist_creator.audio_file_converter import ConversionType
from playlist_creator.playlist_parser import MediaInfoAdapter, PlaylistEntry, TAGS_TO_LOAD

import taglib


def _copy_tag(file: taglib.File, tag: str, metadata: MediaInfoAdapter, make_list=True):
    metadata_tag = metadata.get(tag)
    if metadata_tag:
        file.tags[tag] = [metadata_tag] if make_list else metadata_tag.split(';')


class Tagger:
    playlist_entry: PlaylistEntry
    transcodes_output_directory: str

    def __init__(self, playlist_entry, transcodes_output_directory):
        self.playlist_entry = playlist_entry
        self.transcodes_output_directory = transcodes_output_directory

    def tag(self):
        if self.playlist_entry.conversion_type is not ConversionType.NONE:
            output_location = self.playlist_entry.file_location(self.transcodes_output_directory)
            print(f"Updating tags: {output_location}", flush=True)
            with taglib.File(output_location, save_on_exit=True) as file:
                file.tags = dict()
                for tag in TAGS_TO_LOAD:
                    _copy_tag(file,
                              tag,
                              self.playlist_entry.get_metadata().media_info_metadata,
                              tag not in ['artist', 'genre', 'producer'])
