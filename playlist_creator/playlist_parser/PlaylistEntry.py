from .MediaInfoAdapter import MediaInfoAdapter
from playlist_creator.audio_file_converter import ConversionType

import os
import soundfile


class PlaylistEntry:
    __media_info_adapter: MediaInfoAdapter = None
    __soundfile: soundfile.SoundFile = None

    def __init__(self, file='', title='', length=''):
        self.file: str = file
        self.title: str = title
        self.length: str = length
        self._conversion_type = ConversionType.NONE
        self._load_conversion_type_attempted: bool = False

    @property
    def conversion_type(self):
        return self._conversion_type

    @property
    def metadata_successfully_loaded(self) -> bool:
        return self._media_info_adapter.contains_metadata()

    def add_conversion_type(self, conversion_type: ConversionType):
        if ConversionType.NONE in self._conversion_type or conversion_type is ConversionType.NONE:
            self._conversion_type = conversion_type
        else:
            self._conversion_type = self._conversion_type | conversion_type

    def file_location(self, output_directory: str) -> str:
        return self.file if ConversionType.NONE in self._conversion_type else self.transcoded_file(output_directory)

    def get_conversion_type(self, allowed_formats) -> ConversionType:
        if not self._load_conversion_type_attempted:
            self._determine_conversion_type(allowed_formats)
            self._load_conversion_type_attempted = True

        return self._conversion_type

    def transcoded_file(self, output_directory: str) -> str:
        filename = self._media_info_adapter.formatted_filename()

        return os.path.join(
            output_directory,
            filename + ('.wav' if ConversionType.WAV in self._conversion_type else self._extension())
        ) if filename else ''

    def _determine_conversion_type(self, allowed_formats):
        if self.file:
            print(f"Determining conversion type for: {self.file}", flush=True)

        if self.metadata_successfully_loaded:
            playlist_entry_soundfile = self._soundfile

            if playlist_entry_soundfile.format not in allowed_formats:
                self.add_conversion_type(ConversionType.WAV)
            if isinstance(playlist_entry_soundfile.samplerate, int) and playlist_entry_soundfile.samplerate > 48000:
                self.add_conversion_type(ConversionType.DOWNSAMPLE)
            if playlist_entry_soundfile.subtype == 'PCM_24':
                self.add_conversion_type(ConversionType.BIT_24)

    @property
    def _media_info_adapter(self) -> MediaInfoAdapter:
        if not self.__media_info_adapter:
            self.__media_info_adapter = MediaInfoAdapter(filename=self.file, cmd='ffprobe')

        return self.__media_info_adapter

    @_media_info_adapter.setter
    def _media_info_adapter(self, media_info: MediaInfoAdapter):
        self.__media_info_adapter = media_info

    @property
    def _soundfile(self) -> soundfile.SoundFile:
        if not self.__soundfile:
            self.__soundfile = soundfile.SoundFile(self.file)

        return self.__soundfile

    def _extension(self) -> str:
        split_filename = os.path.splitext(self.file)
        return split_filename[1] if len(split_filename) > 1 else ''

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.file == other.file

    def __hash__(self):
        return hash(self.file)
