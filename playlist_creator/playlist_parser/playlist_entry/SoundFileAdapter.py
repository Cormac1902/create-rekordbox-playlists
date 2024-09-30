import contextlib
import multiprocessing
import os

import soundfile

from playlist_creator import audio_file_converter, configuration


class SoundFileAdapter:
    def __init__(self,
                 file = None,
                 lock: multiprocessing.Lock = None,
                 config: configuration.Config = configuration.Config()):
        self._conversion_type: audio_file_converter.ConversionType \
            = audio_file_converter.ConversionType.NONE
        self._format: str | None = None
        self._load_information_attempted: bool = lock is None
        self.__config: configuration.Config = config
        self.__file = file
        self.__lock = lock

    @property
    def conversion_type(self) -> audio_file_converter.ConversionType:
        if not self._load_information_attempted:
            self._load_information()

        return self._conversion_type

    @property
    def format(self) -> str:
        if not self._load_information_attempted:
            self._load_information()

        return self._format

    @property
    def _config(self) -> configuration.Config:
        return self.__config

    @property
    def _file(self):
        return self.__file

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

    def _load_information(self):
        with self._lock:
            if self._load_information_attempted:
                return

            if self._file:  # pragma: no cover
                print(f"Determining conversion type for: {self._file}", flush=True)

            self._load_information_from_soundfile()

            self._load_information_attempted = True

    def _load_information_from_soundfile(self):
        if os.path.exists(self._file):
            with soundfile.SoundFile(self._file) as playlist_entry_soundfile:
                self._format = playlist_entry_soundfile.format
                if self._format not in self._config.allowed_formats:
                    self.add_conversion_type(audio_file_converter.ConversionType.WAV)
                if (isinstance(playlist_entry_soundfile.samplerate, int)
                        and playlist_entry_soundfile.samplerate > 48000):
                    self.add_conversion_type(audio_file_converter.ConversionType.DOWNSAMPLE)
                if playlist_entry_soundfile.subtype == 'PCM_24':
                    self.add_conversion_type(audio_file_converter.ConversionType.BIT_24)
