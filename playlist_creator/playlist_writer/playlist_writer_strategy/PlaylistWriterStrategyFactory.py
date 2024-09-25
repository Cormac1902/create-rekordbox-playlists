#   pylint: disable=too-few-public-methods

from .PlaylistWriterStrategy import PlaylistWriterStrategy


class PlaylistWriterStrategyFactory:
    def __init__(self):
        self._playlist_writer_strategies: dict[PlaylistWriterStrategy] \
            = dict[PlaylistWriterStrategy]()

    def get_writer_strategy(self, strategy) -> PlaylistWriterStrategy:
        if strategy not in self._playlist_writer_strategies:
            self._playlist_writer_strategies[strategy] = strategy()

        return self._playlist_writer_strategies[strategy]

#   pylint: enable=too-few-public-methods
