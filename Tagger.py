import taglib

from ConversionTypeEnum import ConversionType
from MediaInfoMetadata import MediaInfoMetadata, TAGS_TO_LOAD
from PlaylistEntry import PlaylistEntry


def _copy_tag(file: taglib.File, tag: str, metadata: MediaInfoMetadata, make_list=True):
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
                for tag in TAGS_TO_LOAD:
                    _copy_tag(file, tag, self.playlist_entry.metadata.raw_metadata,
                              tag not in ['artist', 'genre', 'producer'])
