import contextlib
import multiprocessing
import os

from playlist_creator import audio_file_converter
from . import metadata_adapter
from .PlaylistEntryData import PlaylistEntryData
from .SoundFileAdapter import SoundFileAdapter


class PlaylistEntry:
    def __init__(self,
                 lock: multiprocessing.Lock = None,
                 playlist_entry_data: PlaylistEntryData = PlaylistEntryData(),
                 soundfile_adapter: SoundFileAdapter = SoundFileAdapter(),
                 media_info_strategy_factory: metadata_adapter.MediaInfoStrategyFactory = None):
        self._media_info_strategy_factory = media_info_strategy_factory
        self._playlist_entry_data = playlist_entry_data
        self.__lock = lock
        self._soundfile_adapter = soundfile_adapter
        self.__metadata_adapter = None

    def conversion_type(self) -> audio_file_converter.ConversionType:
        return self._soundfile_adapter.conversion_type

    def conversion_type_is_none(self) -> bool:
        return audio_file_converter.ConversionType.NONE in self.conversion_type()

    def format(self) -> str:
        return self._soundfile_adapter.format

    def metadata_successfully_loaded(self) -> bool:
        return self._metadata_adapter().contains_metadata

    def file(self) -> str:
        return self._playlist_entry_data.file

    def length(self) -> str:
        return self._playlist_entry_data.length

    def title(self) -> str:
        return self._playlist_entry_data.title

    def get_metadata(self):
        self._metadata_adapter().load_metadata()

    @property
    def _lock(self):
        return self.__lock if self.__lock else contextlib.nullcontext()

    def _metadata_adapter(self) -> metadata_adapter.MetadataAdapter:
        if not self.__metadata_adapter:
            self.__metadata_adapter = metadata_adapter.MetadataAdapter(
                self._media_info_strategy_factory.get_strategy(
                    metadata_adapter.MediaInfoStrategy
                    if self.format() in metadata_adapter.media_info_strategy.MEDIA_INFO_STRATEGY_FORMATS
                    else metadata_adapter.FfprobeStrategy
                ) if self._media_info_strategy_factory else None,
                self.file(),
                self._lock
            )

        return self.__metadata_adapter

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

    def transcoded_file_exists(self, output_directory) -> bool:
        return os.path.isfile(self.transcoded_file(output_directory))

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
