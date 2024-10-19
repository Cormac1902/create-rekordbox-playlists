import logging

from playlist_creator import audio_file_converter, playlist_parser
from ..PostProcessor import PostProcessor

logger = logging.getLogger(__name__)


class EnhancedMultichannelAudioFixer(PostProcessor):
    def __init__(self, successor: PostProcessor = None):
        super().__init__(successor)

    def process(self,
                playlist_entry: playlist_parser.PlaylistEntry,
                transcodes_output_directory: str):
        if (
                playlist_entry.metadata_successfully_loaded() and
                audio_file_converter.ConversionType.WAV in playlist_entry.conversion_type()
        ):
            output_location = playlist_entry.file_location(transcodes_output_directory)

            with open(output_location, 'r+b') as file:
                file.seek(20)

                enhanced_multichannel_audio_fix_bytes = bytes([0x01, 0x00])

                if bytes(file.read(2)) != enhanced_multichannel_audio_fix_bytes:
                    logger.info(f"Fixing enhanced multichannel audio: {output_location}")
                    file.seek(20)
                    file.write(enhanced_multichannel_audio_fix_bytes)
