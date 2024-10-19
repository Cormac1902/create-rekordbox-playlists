import os
import unittest
from unittest.mock import MagicMock

from playlist_creator import playlist_parser
from tests.playlist_parser.playlist_entry.metadata_adapter.TestMediaInfoStrategy import \
    ConcreteTestMediaInfoStrategy


class TestIMediaInfoStrategy(unittest.TestCase):
    def test_get_metadata_returns_if_filepath_does_not_exist(self):
        test_media_info_strategy = ConcreteTestMediaInfoStrategy()
        os.path.exists = MagicMock(return_value=False)

        self.assertEqual({}, test_media_info_strategy.get_metadata(''))
        test_media_info_strategy._get_cmd.assert_not_called()

    def test_get_metadata_returns_correctly(self):
        test_media_info_strategy = ConcreteTestMediaInfoStrategy()
        test_filename = 'Test'
        test_tag = 'title'
        os.path.exists = MagicMock(return_value=True)
        test_media_info_strategy._get_cmd.return_value = f"test {test_filename}"
        test_media_info_strategy._get_metadata_from_cmd.return_value = {test_tag: test_filename}

        self.assertEqual(
            test_media_info_strategy.get_metadata(test_filename)[test_tag],
            test_filename
        )

    def test_get_metadata_only_returns_tags_to_load(self):
        test_media_info_strategy = ConcreteTestMediaInfoStrategy()
        test_filename = 'Test'
        test_tag = 'title_2'
        os.path.exists = MagicMock(return_value=True)
        test_media_info_strategy._get_cmd.return_value = f"test {test_filename}"
        test_media_info_strategy._get_metadata_from_cmd.return_value = {test_tag: test_filename}

        self.assertFalse(test_tag in test_media_info_strategy.get_metadata(test_filename))

    def test_get_metadata_returns_none_for_empty_tags(self):
        test_media_info_strategy = ConcreteTestMediaInfoStrategy()
        os.path.exists = MagicMock(return_value=True)
        test_media_info_strategy._get_metadata_from_cmd.return_value = {}

        self.assertEqual(
            {tag: None for tag in playlist_parser.TAGS_TO_LOAD},
            test_media_info_strategy.get_metadata('')
        )

    def test_get_metadata_returns_empty_dict_if_metadata_is_empty(self):
        import logging

        logging.basicConfig(level=logging.ERROR)

        test_media_info_strategy = ConcreteTestMediaInfoStrategy()
        os.path.exists = MagicMock(return_value=True)
        test_media_info_strategy._get_metadata_from_cmd.return_value = None

        self.assertEqual({}, test_media_info_strategy.get_metadata(''))

        logging.basicConfig(level=logging.WARNING)


if __name__ == '__main__':
    unittest.main()
