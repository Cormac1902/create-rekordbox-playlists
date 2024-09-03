from playlist_creator import audio_file_converter, playlist_parser, ConversionType

import unittest


class TestPlaylistEntry(unittest.TestCase):
    def test_conversion_type_is_initialised_to_none(self):
        test_playlist_entry = playlist_parser.PlaylistEntry()

        self.assertEqual(test_playlist_entry.conversion_type, ConversionType.NONE)

    def test_add_conversion_type_clears_none(self):
        test_playlist_entry = playlist_parser.PlaylistEntry()

        test_playlist_entry.add_conversion_type(ConversionType.WAV)

        self.assertNotIn(ConversionType.NONE, test_playlist_entry.conversion_type)

    def test_adding_none_conversion_type_clears_existing(self):
        test_playlist_entry = playlist_parser.PlaylistEntry()

        test_playlist_entry.add_conversion_type(ConversionType.WAV)
        test_playlist_entry.add_conversion_type(ConversionType.NONE)

        self.assertEqual(ConversionType.NONE, test_playlist_entry.conversion_type)

    def test_add_conversion_type_adds_conversion_type(self):
        test_playlist_entry = playlist_parser.PlaylistEntry()

        test_playlist_entry.add_conversion_type(ConversionType.WAV)

        self.assertIn(ConversionType.WAV, test_playlist_entry.conversion_type)

    def test_add_conversion_type_adds_multiple_conversion_types(self):
        test_playlist_entry = playlist_parser.PlaylistEntry()

        test_playlist_entry.add_conversion_type(ConversionType.WAV)
        test_playlist_entry.add_conversion_type(ConversionType.BIT_24)

        self.assertIn(ConversionType.WAV, test_playlist_entry.conversion_type)
        self.assertIn(ConversionType.BIT_24, test_playlist_entry.conversion_type)


if __name__ == '__main__':
    unittest.main()
