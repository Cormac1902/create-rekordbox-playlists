from playlist_creator.audio_file_converter import ConversionType
from playlist_creator.playlist_parser.PlaylistEntry import PlaylistEntry


class EnhancedMultichannelAudioFixer:
    playlist_entry: PlaylistEntry
    transcodes_output_directory: str

    def __init__(self, playlist_entry, transcodes_output_directory):
        self.playlist_entry = playlist_entry
        self.transcodes_output_directory = transcodes_output_directory

    def fix(self):
        if ConversionType.WAV in self.playlist_entry.conversion_type:
            output_location = self.playlist_entry.file_location(self.transcodes_output_directory)

            print(f"Fixing enhanced multichannel audio: {output_location}", flush=True)

            with open(output_location, 'r+b') as file:
                file.seek(20)
                file.write(bytes([0x01, 0x00]))
