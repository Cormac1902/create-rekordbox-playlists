import os

from ConversionTypeEnum import ConversionType
from PlaylistEntryMetadata import PlaylistEntryMetadata


class PlaylistEntry:
    metadata: PlaylistEntryMetadata
    conversion_type: ConversionType = ConversionType.NONE

    def __init__(self, file, title, length):
        self.file: str = file
        self.title: str = title
        self.length: str = length

    def add_conversion_type(self, conversion_type: ConversionType):
        if ConversionType.NONE in self.conversion_type or conversion_type is ConversionType.NONE:
            self.conversion_type = conversion_type
        else:
            self.conversion_type = self.conversion_type | conversion_type

    def extension(self) -> str:
        return os.path.splitext(self.file)[1]

    def transcoded_file(self, output_directory) -> str:
        return os.path.join(output_directory,
                            self.metadata.filename().replace('.', r'\.') +
                            ('.wav' if ConversionType.WAV in self.conversion_type else self.extension()))
