#   pylint: disable=too-few-public-methods

from .IMediaInfoStrategy import IMediaInfoStrategy


class MediaInfoStrategyFactory:
    def __init__(self):
        self._strategies: dict[IMediaInfoStrategy] = dict[IMediaInfoStrategy]()

    def get_strategy(self, strategy) -> IMediaInfoStrategy:
        if strategy not in self._strategies:
            self._strategies[strategy] = strategy()

        return self._strategies[strategy]

#   pylint: enable=too-few-public-methods
