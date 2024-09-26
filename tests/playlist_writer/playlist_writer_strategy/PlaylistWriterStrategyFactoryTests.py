import unittest

from playlist_creator import playlist_writer
from .TestPlaylistWriterStrategy import TestPlaylistWriterStrategy


class TestPlaylistWriterStrategyFactory(unittest.TestCase):
    def test_get_writer_strategy_instantiates_strategy(self):
        test_playlist_writer_strategy_factory = playlist_writer.PlaylistWriterStrategyFactory()

        self.assertIsInstance(
            test_playlist_writer_strategy_factory.get_writer_strategy(TestPlaylistWriterStrategy),
            TestPlaylistWriterStrategy
        )


if __name__ == '__main__':
    unittest.main()
