#   pylint: disable=too-few-public-methods

from .ConverterStrategy import ConverterStrategy


class ConverterStrategyFactory:
    def __init__(self):
        self._converter_strategies: dict[ConverterStrategy] = dict[ConverterStrategy]()

    def get_strategy(self, strategy, **kwargs) -> ConverterStrategy:
        if strategy not in self._converter_strategies:
            self._converter_strategies[strategy] = strategy(**kwargs)

        return self._converter_strategies[strategy]

#   pylint: enable=too-few-public-methods
