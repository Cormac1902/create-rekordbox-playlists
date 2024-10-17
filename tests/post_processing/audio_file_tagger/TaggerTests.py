import unittest
import unittest.mock
from unittest.mock import MagicMock

from playlist_creator import post_processing


class TestTagger(unittest.TestCase):
    def test_when_process_is_called_file_tags_are_updated(self):
        with unittest.mock.patch('taglib.File') as mock_taglib_file:
            with mock_taglib_file.return_value as mock_taglib_return:
                test_tag = 'title'
                test_tags = {test_tag: ['Test 1']}

                mock_taglib_return.tags = test_tags

                test_tagger = post_processing.Tagger()
                test_playlist_entry = MagicMock()
                test_tag_value = 'Test 2'
                test_playlist_entry.get_metadata_tag = MagicMock(return_value=test_tag_value)

                self.assertNotEqual(mock_taglib_return.tags[test_tag], [test_tag_value])

                test_tagger.process(test_playlist_entry, str())

                self.assertEqual(mock_taglib_return.tags[test_tag], [test_tag_value])


if __name__ == '__main__':
    unittest.main()
