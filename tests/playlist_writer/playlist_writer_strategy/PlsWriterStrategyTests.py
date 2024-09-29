import os
import unittest
from unittest.mock import MagicMock, call, patch

from playlist_creator import playlist_parser, playlist_writer


class TestPlsWriterStrategy(unittest.TestCase):
    def test_get_writer_strategy_instantiates_strategy(self):
        test_pls_writer_strategy = playlist_writer.PlsWriterStrategy()
        test_title = 'Test title'
        test_filepath = '/test'
        test_transcodes_output_directory = '/test2'
        test_file = os.sep.join([test_filepath, f"{test_title}.flac"])
        test_playlist_filename = os.sep.join([test_filepath, f"{test_title}.pls"])
        test_length = '100'
        test_playlist_entry = playlist_parser.PlaylistEntry(
            playlist_entry_data=playlist_parser.PlaylistEntryData(
                test_file, test_title, test_length
            )
        )
        test_playlist = playlist_parser.Playlist(
            test_title, test_length, [test_playlist_entry]
        )
        test_playlist_entry.file_location = MagicMock(return_value=test_filepath)
        test_playlist_entry.metadata_successfully_loaded = MagicMock(return_value=True)

        with patch("builtins.open", unittest.mock.mock_open(read_data="data")) as mock_open:
            test_pls_writer_strategy.write_playlist(
                test_playlist,
                test_filepath,
                test_transcodes_output_directory
            )

            mock_open.assert_called_once_with(
                test_playlist_filename,
                mode='w',
                encoding='utf-8'
            )
            mock_open.return_value.write.assert_has_calls([call('[playlist]\n')])
            mock_open.return_value.writelines.assert_has_calls(
                [
                    call([
                        f"File1={test_playlist_entry.file_location(test_transcodes_output_directory)}\n",
                        f"Title1={test_playlist_entry.title()}\n",
                        f"Length1={test_playlist_entry.length()}\n"
                    ]),
                    call([
                        'NumberOfEntries=1\n',
                        'Version=2'
                    ])
                ],
            )

    def test_hash(self):
        self.assertEqual(hash(playlist_writer.PlsWriterStrategy()), hash('pls'))



if __name__ == '__main__':
    unittest.main()
