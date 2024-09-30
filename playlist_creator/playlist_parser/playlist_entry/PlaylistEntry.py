import contextlib
import multiprocessing
import os

import soundfile

from playlist_creator import audio_file_converter, configuration
from . import metadata_adapter
from .PlaylistEntryData import PlaylistEntryData


class PlaylistEntry:
    def __init__(self,
                 lock: multiprocessing.RLock = None,
                 playlist_entry_data: PlaylistEntryData = PlaylistEntryData(),
                 config: configuration.Config = configuration.Config(),
                 media_info_strategy_factory: metadata_adapter.MediaInfoStrategyFactory = None):
        self._media_info_strategy_factory = media_info_strategy_factory
        self._playlist_entry_data = playlist_entry_data
        self.__lock = lock
        self.__metadata_adapter = None
        self.__config: configuration.Config = config
        self._conversion_type: audio_file_converter.ConversionType \
            = audio_file_converter.ConversionType.NONE
        self._format: str | None = None
        self._load_conversion_type_attempted: bool = False

    def conversion_type(self) -> audio_file_converter.ConversionType:
        if not self._load_conversion_type_attempted:
            self._determine_conversion_type()

        return self._conversion_type

    def format(self) -> str:
        if not self._load_conversion_type_attempted:
            self._determine_conversion_type()

        return self._format

    def metadata_successfully_loaded(self) -> bool:
        return self._metadata_adapter().contains_metadata

    def file(self) -> str:
        return self._playlist_entry_data.file

    def length(self) -> str:
        return self._playlist_entry_data.length

    def title(self) -> str:
        return self._playlist_entry_data.title

    @property
    def _config(self) -> configuration.Config:
        return self.__config

    @property
    def _lock(self):
        return self.__lock if self.__lock else contextlib.nullcontext()

    def _metadata_adapter(self):
        if not self.__metadata_adapter:
            self.__metadata_adapter = metadata_adapter.MetadataAdapter(
                self._media_info_strategy_factory.get_strategy(
                    metadata_adapter.MediaInfoStrategy
                    if self.format() in metadata_adapter.MEDIA_INFO_STRATEGY_FORMATS
                    else metadata_adapter.FfprobeStrategy
                ) if self._media_info_strategy_factory else None,
                self.file(),
                self._lock
            )

        return self.__metadata_adapter

    def add_conversion_type(self, conversion_type: audio_file_converter.ConversionType):
        if (
                audio_file_converter.ConversionType.NONE in self._conversion_type or
                conversion_type is audio_file_converter.ConversionType.NONE
        ):
            self._conversion_type = conversion_type
        else:
            self._conversion_type = self._conversion_type | conversion_type

    def file_location(self, output_directory: str) -> str:
        return self.file() if audio_file_converter.ConversionType.NONE in self.conversion_type() \
            else self.transcoded_file(output_directory)

    def get_metadata_tag(self, key) -> str | None:
        return self._metadata_adapter().get(key)

    def transcoded_file(self, output_directory: str) -> str:
        filename = self._metadata_adapter().formatted_filename()

        return os.path.join(
            output_directory,
            f"{filename}"
            f"{".wav"
            if audio_file_converter.ConversionType.WAV in self.conversion_type()
            else self._extension()
            }"
        ) if filename else ''

    def _determine_conversion_type(self):
        with self._lock:
            if self._load_conversion_type_attempted:
                return

            if self.file():  # pragma: no cover
                print(f"Determining conversion type for: {self.file()}", flush=True)

            self._determine_conversion_type_from_soundfile()

            self._load_conversion_type_attempted = True

    def _determine_conversion_type_from_soundfile(self):
        with soundfile.SoundFile(self.file()) as playlist_entry_soundfile:
            self._format = playlist_entry_soundfile.format
            if self._format not in self._config.allowed_formats:
                self.add_conversion_type(audio_file_converter.ConversionType.WAV)
            if (isinstance(playlist_entry_soundfile.samplerate, int)
                    and playlist_entry_soundfile.samplerate > 48000):
                self.add_conversion_type(audio_file_converter.ConversionType.DOWNSAMPLE)
            if playlist_entry_soundfile.subtype == 'PCM_24':
                self.add_conversion_type(audio_file_converter.ConversionType.BIT_24)

    def _extension(self) -> str:
        file = self.file()
        split_filename = os.path.splitext(file) if file else ''
        return split_filename[1] if len(split_filename) > 1 else ''

    def __eq__(self, other) -> bool:
        if not isinstance(other, type(self)):
            return NotImplemented
        return self._playlist_entry_data == other._playlist_entry_data

    def __hash__(self) -> int:
        return hash(self._playlist_entry_data)
