import os
import sys
import unittest
sys.path.insert(
    0,
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from spycis import wrappers
from spycis.wrappers.common import BaseWrapper, Media, Stream


class TubeplusTests(unittest.TestCase):

    def test_tubepluswrapper_exists(self):
        site = wrappers.get_instance("tubeplus")
        self.assertIsInstance(site, BaseWrapper)

    def test_tubeplus_search_return_expected_dict(self):
        site = wrappers.get_instance("tubeplus")
        medias = site.search("The Animal Kingdom")

        self.assertIsInstance(medias, list)
        self.assertGreater(len(medias), 0)

        self.assertTrue(all(isinstance(m, Media) for m in medias))

    def test_tubeplus_get_stream_urls_from_media_page_returns_valid_streams(self):
        media_url = "http://www.tubeplus.me/player/2132628/"
        site = wrappers.get_instance("tubeplus")
        streams = list(site.get_streams(media_url=media_url, code="s01e02"))

        self.assertGreater(len(streams), 0)

        self.assertTrue(
            all(True if isinstance(s, Stream) else False for s in streams))


class LoveSerieTests(unittest.TestCase):

    def test_loveserie_wrapper_exists(self):
        from spycis.wrappers.common import BaseWrapper
        site = wrappers.get_instance("loveserie")
        self.assertIsInstance(site, BaseWrapper)

    def test_loveserie_search_return_valid_medias(self):
        site = wrappers.get_instance("loveserie")
        medias = site.search("wood")

        self.assertIsInstance(medias, list)
        self.assertGreater(len(medias), 0)

        for media in medias:
            self.assertIsInstance(media, Media)

        titles = ('Deadwood', 'Torchwood', 'Hollywood Girls',
                  'Les Chtis a Hollywood (saison 5)', 'Ravenswood')
        self.assertTrue(
            all(True if m.title in titles else False for m in medias))

    def test_loveserie_get_stream_urls_from_media_url_returns_valid_streams(self):
        # media_url = "http://www.loveserie.com/streaming-6104"
        media_url = "http://www.loveserie.com/streaming-9317"
        site = wrappers.get_instance("loveserie")
        streams = list(site.get_streams(media_url=media_url, code="s01e02"))

        self.assertGreater(len(streams), 0)
        self.assertTrue(
            all(True if isinstance(s, Stream) else False for s in streams))

        first_stream = streams[0]

        expected_stream = Stream(
            url='http://youwatch.org/yso5atvraz7e',
            language='French',
            subtitles=[],
            hd=False,)
        self.assertEqual(first_stream.url, expected_stream.url)
        self.assertEqual(first_stream.language, expected_stream.language)
        self.assertEqual(first_stream.subtitles, expected_stream.subtitles)
        self.assertEqual(first_stream.hd, expected_stream.hd)


if __name__ == "__main__":
    unittest.main()
