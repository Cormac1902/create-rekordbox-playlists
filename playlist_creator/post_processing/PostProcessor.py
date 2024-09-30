from abc import abstractmethod

from playlist_creator import playlist_parser


class PostProcessor:
    def __init__(self, successor):
        self._successor: PostProcessor = successor

    def process_chain(self,
                playlist_entry: playlist_parser.PlaylistEntry,
                transcodes_output_directory: str):
        self.process(playlist_entry, transcodes_output_directory)

        if self._successor:
            self._successor.process(playlist_entry, transcodes_output_directory)

    @abstractmethod
    def process(self,
                playlist_entry: playlist_parser.PlaylistEntry,
                transcodes_output_directory: str):
        pass
