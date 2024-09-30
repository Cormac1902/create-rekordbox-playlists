import unittest

from playlist_creator import playlist_parser
from tests.playlist_parser.playlist_entry.metadata_adapter.TestMediaInfoStrategy import \
    TestMediaInfoStrategy


class TestMediaInfoStrategyFactory(unittest.TestCase):
    def test_get_strategy_instantiates_strategy(self):
        test_playlist_writer_strategy_factory = playlist_parser.MediaInfoStrategyFactory()

        self.assertIsInstance(
            test_playlist_writer_strategy_factory.get_strategy(TestMediaInfoStrategy),
            TestMediaInfoStrategy
        )


if __name__ == '__main__':
    unittest.main()
