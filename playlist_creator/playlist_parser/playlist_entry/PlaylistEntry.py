import contextlib
import multiprocessing.managers
import os

import soundfile

from playlist_creator import audio_file_converter, configuration
from .MediaInfoAdapter import MediaInfoAdapter
from .PlaylistEntryData import PlaylistEntryData


class PlaylistEntry:
    _media_info_adapter: MediaInfoAdapter = MediaInfoAdapter()
    __lock: multiprocessing.Lock = None
    __soundfile: soundfile.SoundFile | None = None

    def __init__(self,
                 manager: multiprocessing.Manager = None,
                 playlist_entry_data: PlaylistEntryData = PlaylistEntryData(),
                 config: configuration.Config = None):
        self._playlist_entry_data = playlist_entry_data

        if manager:
            self.__lock = manager.Lock()
            self._media_info_adapter = MediaInfoAdapter(
                manager.Lock(),
                manager.dict(),
                filename=self.file,
                cmd='ffprobe'
            )

        self.__config: configuration.Config = config
        self._conversion_type: audio_file_converter.ConversionType \
            = audio_file_converter.ConversionType.NONE
        self._load_conversion_type_attempted: bool = False

    @property
    def conversion_type(self) -> audio_file_converter.ConversionType:
        if not self._load_conversion_type_attempted:
            self._determine_conversion_type()
            self._load_conversion_type_attempted = True

        return self._conversion_type

    @property
    def metadata_successfully_loaded(self) -> bool:
        return self._media_info_adapter.contains_metadata()

    @property
    def file(self) -> str:
        return self._playlist_entry_data.file

    @property
    def length(self) -> str:
        return self._playlist_entry_data.length

    @property
    def title(self) -> str:
        return self._playlist_entry_data.title

    @property
    def _config(self) -> configuration.Config:
        return self.__config

    @property
    def _lock(self):
        return self.__lock if self.__lock else contextlib.nullcontext()

    def add_conversion_type(self, conversion_type: audio_file_converter.ConversionType):
        if (
                audio_file_converter.ConversionType.NONE in self._conversion_type or
                conversion_type is audio_file_converter.ConversionType.NONE
        ):
            self._conversion_type = conversion_type
        else:
            self._conversion_type = self._conversion_type | conversion_type

    def file_location(self, output_directory: str) -> str:
        return self.file if audio_file_converter.ConversionType.NONE in self.conversion_type \
            else self.transcoded_file(output_directory)

    def get_metadata_tag(self, key) -> str | None:
        return self._media_info_adapter.get(key)

    def transcoded_file(self, output_directory: str) -> str:
        filename = self._media_info_adapter.formatted_filename()

        return os.path.join(
            output_directory,
            f"{filename}"
            f"{".wav"
            if audio_file_converter.ConversionType.WAV in self.conversion_type
            else self._extension()
            }"
        ) if filename else ''

    def _determine_conversion_type(self):
        if self.file:  # pragma: no cover
            print(f"Determining conversion type for: {self.file}", flush=True)

        if self.metadata_successfully_loaded:
            with self._lock:
                playlist_entry_soundfile = self._soundfile

                if playlist_entry_soundfile.format not in self._config.allowed_formats:
                    self.add_conversion_type(audio_file_converter.ConversionType.WAV)
                if (isinstance(playlist_entry_soundfile.samplerate, int)
                        and playlist_entry_soundfile.samplerate > 48000):
                    self.add_conversion_type(audio_file_converter.ConversionType.DOWNSAMPLE)
                if playlist_entry_soundfile.subtype == 'PCM_24':
                    self.add_conversion_type(audio_file_converter.ConversionType.BIT_24)

                self.__soundfile = None

    @property
    def _soundfile(self) -> soundfile.SoundFile:
        if not self.__soundfile:
            self.__soundfile = soundfile.SoundFile(self.file)

        return self.__soundfile

    def _extension(self) -> str:
        split_filename = os.path.splitext(self.file) if self.file else ''
        return split_filename[1] if len(split_filename) > 1 else ''

    def __eq__(self, other) -> bool:
        if not isinstance(other, type(self)):
            return NotImplemented
        return self._playlist_entry_data == other._playlist_entry_data

    def __hash__(self) -> int:
        return hash(self._playlist_entry_data)
