import os
import sys
import unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from spycis import wrappers
from spycis.wrappers.common import Media


class TubeplusTests(unittest.TestCase):

    def test_tubepluswrapper_exists(self):
        from spycis.wrappers.common import BaseWrapper
        site = wrappers.get_instance("tubeplus")
        self.assertIsInstance(site, BaseWrapper)

    def test_tubeplus_search_return_expected_dict(self):
        site = wrappers.get_instance("tubeplus")
        search_results = site.search("The Animal Kingdom")

        self.assertIsInstance(search_results, list)
        self.assertGreater(len(search_results), 0)
        for result in search_results:
            self.assertIsInstance(result, dict)
        for result in search_results:
            self.assertIsNotNone(result.get('title'))
            self.assertIsNotNone(result.get('url'))
            self.assertIsNotNone(result.get('description'))
            self.assertIsNotNone(result.get('thumbnail'))
            self.assertIsNotNone(result.get('tags'))
            self.assertIsNotNone(result.get('year'))
            self.assertIsNotNone(result.get('rating'))

        expected_dict = {
            'title': 'The Animal Kingdom',
            'description': 'The Animal Kingdom Tom Collier has had a great relationship with Daisy, but when he decides to marry, it is not Daisy whom he asks, it is Cecelia. After the marriage, Tom is bored with the social scene and the obligatio...',
            'year': '1932',
            'url': 'http://www.tubeplus.me/player/523193/The_Animal_Kingdom/',
            'rating': 0.65,
            'tags': ['film'],
            'thumbnail': 'http://www.tubeplus.me/resources/thumbs/523193.jpg'
        }

        self.assertIn(expected_dict, search_results)

    def test_tubeplus_get_urls_return_valid_urls(self):
        url = "http://www.tubeplus.me/player/40142/Animal_Kingdom/"
        site = wrappers.get_instance("tubeplus")
        urls = site.get_urls(url)

        for url in urls:
            self.assertTrue(url.startswith('http://'))


class LoveSerieTests(unittest.TestCase):

    def test_loveserie_wrapper_exists(self):
        from spycis.wrappers.common import BaseWrapper
        site = wrappers.get_instance("loveserie")
        self.assertIsInstance(site, BaseWrapper)

    def test_loveserie_search_return_expected_dict(self):
        site = wrappers.get_instance("loveserie")
        search_results = site.search("dead")

        self.assertIsInstance(search_results, list)
        self.assertGreater(len(search_results), 0)

        for result in search_results:
            self.assertIsInstance(result, Media)

        # self.assertIn(expected_dict, search_results)

    def test_loveserie_get_stream_urls_from_media_page(self):
        media_url = "http://www.loveserie.com/streaming-6104"
        site = wrappers.get_instance("loveserie")
        stream_urls = site.get_urls(url=media_url, code="s03e10")

        self.assertIsInstance(stream_urls, list)

if __name__ == "__main__":
    unittest.main()
