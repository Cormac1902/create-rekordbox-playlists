from .MediaInfoAdapter import MediaInfoAdapter
from .PlaylistEntryMetadata import PlaylistEntryMetadata
from playlist_creator.audio_file_converter import ConversionType

import os
import soundfile


class PlaylistEntry:
    conversion_type: ConversionType = ConversionType.NONE
    _metadata: PlaylistEntryMetadata = None

    def __init__(self, file='', title='', length=''):
        self.file: str = file
        self.title: str = title
        self.length: str = length

    def add_conversion_type(self, conversion_type: ConversionType):
        if ConversionType.NONE in self.conversion_type or conversion_type is ConversionType.NONE:
            self.conversion_type = conversion_type
        else:
            self.conversion_type = self.conversion_type | conversion_type

    def get_metadata(self) -> PlaylistEntryMetadata:
        if not self._metadata:
            mediainfo = MediaInfoAdapter(filename=self.file, cmd='ffprobe')
            self._metadata = PlaylistEntryMetadata(mediainfo)

        return self._metadata

    def processed(self) -> bool:
        return self.get_metadata().contains_metadata()

    def transcoded_file(self, output_directory: str) -> str:
        filename = self.get_metadata().filename()

        return os.path.join(
            output_directory,
            filename + ('.wav' if ConversionType.WAV in self.conversion_type else self._extension())
        ) if filename else ''

    def file_location(self, output_directory: str) -> str:
        return self.file if ConversionType.NONE in self.conversion_type else self.transcoded_file(output_directory)

    def determine_conversion_type(self, allowed_formats, playlist_entry_soundfile: soundfile.SoundFile):
        print(f"Determining conversion type for: {self.file}", flush=True)

        if self.processed():
            if playlist_entry_soundfile.format not in allowed_formats:
                self.add_conversion_type(ConversionType.WAV)
            if isinstance(playlist_entry_soundfile.samplerate, int) and playlist_entry_soundfile.samplerate > 48000:
                self.add_conversion_type(ConversionType.DOWNSAMPLE)
            if playlist_entry_soundfile.subtype == 'PCM_24':
                self.add_conversion_type(ConversionType.BIT_24)

    def _extension(self) -> str:
        split_filename = os.path.splitext(self.file)
        return split_filename[1] if len(split_filename) > 1 else ''

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.file == other.file

    def __hash__(self):
        return hash(self.file)
