import contextlib
import multiprocessing
import os

import soundfile

from playlist_creator import audio_file_converter, configuration
from .MediaInfoAdapter import MediaInfoAdapter
from .PlaylistEntryData import PlaylistEntryData


class PlaylistEntry:
    __soundfile: soundfile.SoundFile | None = None

    def __init__(self,
                 lock: multiprocessing.RLock = None,
                 playlist_entry_data: PlaylistEntryData = PlaylistEntryData(),
                 config: configuration.Config = configuration.Config()):
        self._playlist_entry_data = playlist_entry_data
        self.__lock = lock
        self._media_info_adapter = MediaInfoAdapter(
            self._lock,
            filename=self.file(),
            cmd='ffprobe'
        )

        self.__config: configuration.Config = config
        self._conversion_type: audio_file_converter.ConversionType \
            = audio_file_converter.ConversionType.NONE
        self._load_conversion_type_attempted: bool = False

    def conversion_type(self) -> audio_file_converter.ConversionType:
        if not self._load_conversion_type_attempted:
            self._determine_conversion_type()

        return self._conversion_type

    def metadata_successfully_loaded(self) -> bool:
        return self._media_info_adapter.contains_metadata()

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
        return self._media_info_adapter.get(key)

    def transcoded_file(self, output_directory: str) -> str:
        filename = self._media_info_adapter.formatted_filename()

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

            if self.metadata_successfully_loaded():
                playlist_entry_soundfile = self._soundfile()

                if playlist_entry_soundfile.format not in self._config.allowed_formats:
                    self.add_conversion_type(audio_file_converter.ConversionType.WAV)
                if (isinstance(playlist_entry_soundfile.samplerate, int)
                        and playlist_entry_soundfile.samplerate > 48000):
                    self.add_conversion_type(audio_file_converter.ConversionType.DOWNSAMPLE)
                if playlist_entry_soundfile.subtype == 'PCM_24':
                    self.add_conversion_type(audio_file_converter.ConversionType.BIT_24)

                self.__soundfile = None

            self._load_conversion_type_attempted = True

    def _soundfile(self) -> soundfile.SoundFile:
        if not self.__soundfile:
            self.__soundfile = soundfile.SoundFile(self.file())

        return self.__soundfile

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
