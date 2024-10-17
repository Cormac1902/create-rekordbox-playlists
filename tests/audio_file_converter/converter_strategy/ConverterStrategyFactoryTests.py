import unittest

from playlist_creator import audio_file_converter
from .TestConverterStrategy import TestConverterStrategy


class TestConverterStrategyFactory(unittest.TestCase):
    def test_get_writer_strategy_instantiates_strategy(self):
        test_playlist_writer_strategy_factory = audio_file_converter.ConverterStrategyFactory()

        self.assertIsInstance(
            test_playlist_writer_strategy_factory.get_strategy(TestConverterStrategy),
            TestConverterStrategy
        )


if __name__ == '__main__':
    unittest.main()
