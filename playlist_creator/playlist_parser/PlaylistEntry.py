from .MediaInfoMetadata import MediaInfoMetadata
from .PlaylistEntryMetadata import PlaylistEntryMetadata
from playlist_creator.audio_file_converter import ConversionType

import os
import soundfile


class PlaylistEntry:
    metadata: PlaylistEntryMetadata
    conversion_type: ConversionType = ConversionType.NONE

    def __init__(self, file= '', title = '', length = ''):
        self.file: str = file
        self.title: str = title
        self.length: str = length

    def add_conversion_type(self, conversion_type: ConversionType):
        if ConversionType.NONE in self.conversion_type or conversion_type is ConversionType.NONE:
            self.conversion_type = conversion_type
        else:
            self.conversion_type = self.conversion_type | conversion_type

    def processed(self) -> bool:
        return self.metadata.media_info_metadata.contains_metadata()

    def extension(self) -> str:
        return os.path.splitext(self.file)[1]

    def transcoded_file(self, output_directory) -> str:
        return os.path.join(output_directory,
                            self.metadata.filename() +
                            ('.wav' if ConversionType.WAV in self.conversion_type else self.extension()))

    def file_location(self, output_directory) -> str:
        return self.file if self.conversion_type == ConversionType.NONE else self.transcoded_file(output_directory)

    def determine_conversion_type(self, allowed_formats):
        print(f"Determining conversion type for: {self.file}", flush=True)
        playlist_entry_soundfile = soundfile.SoundFile(self.file)
        mediainfo = MediaInfoMetadata(
            filename=self.file, cmd=r'C:\Program Files\ffmpeg\ffprobe.exe'
        )
        self.metadata = PlaylistEntryMetadata(mediainfo)
        if self.processed():
            if playlist_entry_soundfile.format not in allowed_formats:
                self.add_conversion_type(ConversionType.WAV)
            if playlist_entry_soundfile.samplerate > 48000:
                self.add_conversion_type(ConversionType.DOWNSAMPLE)
            if playlist_entry_soundfile.subtype == 'PCM_24':
                self.add_conversion_type(ConversionType.BIT_24)

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.file == other.file

    def __hash__(self):
        return hash(self.file)
