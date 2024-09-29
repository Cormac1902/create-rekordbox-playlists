from playlist_creator import audio_file_converter, playlist_parser

import taglib


def _copy_tag(file: taglib.File, tag: str, playlist_entry: playlist_parser.PlaylistEntry, make_list=True):
    metadata_tag = playlist_entry.get_metadata_tag(tag)
    if metadata_tag:
        file.tags[tag] = [metadata_tag] if make_list else metadata_tag.split(';')


class Tagger:
    playlist_entry: playlist_parser.PlaylistEntry
    transcodes_output_directory: str

    def __init__(self, playlist_entry, transcodes_output_directory):
        self.playlist_entry = playlist_entry
        self.transcodes_output_directory = transcodes_output_directory

    def tag(self):
        if self.playlist_entry.conversion_type() is not audio_file_converter.ConversionType.NONE:
            output_location = self.playlist_entry.file_location(self.transcodes_output_directory)
            print(f"Updating tags: {output_location}", flush=True)
            with taglib.File(output_location, save_on_exit=True) as file:
                file.tags = dict()
                for tag in playlist_parser.TAGS_TO_LOAD:
                    _copy_tag(file,
                              tag,
                              self.playlist_entry,
                              tag not in ['artist', 'genre', 'producer'])
