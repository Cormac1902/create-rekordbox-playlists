import multiprocessing
import unittest
from unittest.mock import MagicMock

from playlist_creator import configuration, playlist_parser


class TestPlaylistEntryFactory(unittest.TestCase):
    def test_config_is_initialised(self):
        test_config = configuration.Config(set())
        test_playlist_entry_factory = playlist_parser.PlaylistEntryFactory(test_config)

        self.assertEqual(test_playlist_entry_factory._config, test_config)

    def test_manager_is_initialised(self):
        test_manager = multiprocessing.Manager()
        multiprocessing.Manager = MagicMock(return_value=test_manager)
        test_playlist_entry_factory = playlist_parser.PlaylistEntryFactory()

        self.assertEqual(test_playlist_entry_factory._manager, test_manager)

    def test_playlist_entries_is_initialised(self):
        test_manager = multiprocessing.Manager()
        multiprocessing.Manager = MagicMock(return_value=test_manager)
        test_playlist_entries = {}
        test_manager.dict = MagicMock(return_value=test_playlist_entries)
        test_playlist_entry_factory = playlist_parser.PlaylistEntryFactory()

        self.assertEqual(test_playlist_entry_factory.playlist_entries, test_playlist_entries)

    def test_lock_is_initialised(self):
        test_manager = multiprocessing.Manager()
        multiprocessing.Manager = MagicMock(return_value=test_manager)
        test_lock = multiprocessing.Lock()
        test_manager.Lock = MagicMock(return_value=test_lock)
        test_playlist_entry_factory = playlist_parser.PlaylistEntryFactory()

        self.assertEqual(test_playlist_entry_factory._lock, test_lock)

    def test_add_playlist_entry(self):
        test_manager = multiprocessing.Manager()
        multiprocessing.Manager = MagicMock(return_value=test_manager)
        test_playlist_entries = {}
        test_manager.dict = MagicMock(return_value=test_playlist_entries)
        test_playlist_entry_factory = playlist_parser.PlaylistEntryFactory()
        test_playlist_entry = playlist_parser.PlaylistEntry()

        with unittest.mock.patch(
                'playlist_creator.playlist_parser.playlist_entry.PlaylistEntryFactory.PlaylistEntry'

        ) as mock_playlist_entry:
            mock_playlist_entry.return_value=test_playlist_entry

            self.assertEqual(
                test_playlist_entry_factory.add_playlist_entry(playlist_parser.PlaylistEntryData()),
                test_playlist_entry
            )
            mock_playlist_entry.assert_called_once()


if __name__ == '__main__':
    unittest.main()
