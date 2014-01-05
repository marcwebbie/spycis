import os
import sys
import unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from spycis import extractors


class ExtractorsTests(unittest.TestCase):

    def test_get_extractors_by_name(self):
        from spycis.extractors import example
        extractor = extractors.get_extractor(name="example")
        self.assertIsInstance(extractor, example.ExampleExtractor)

    def test_divxstage(self):
        extractor = extractors.get_extractor(name="divxstage")
        self.assertIsNotNone(extractor)

        url = "http://www.divxstage.eu/video/v7f6bhbgvcbgw"

        info = extractor.extract(url)
        self.assertIsInstance(info, dict)

        self.assertIn("id", info.keys())
        self.assertIn("title", info.keys())
        self.assertIn("url", info.keys())
        self.assertIn("ext", info.keys())

    def test_putlocker(self):
        extractor = extractors.get_extractor(name="putlocker")
        self.assertIsNotNone(extractor)

        url = "http://www.putlocker.com/file/B90D29CBE84B2075"

        info = extractor.extract(url)
        self.assertIsInstance(info, dict)

        self.assertIn("id", info.keys())
        self.assertIn("title", info.keys())
        self.assertIn("url", info.keys())
        self.assertIn("ext", info.keys())

    def test_nowvideo(self):
        extractor = extractors.get_extractor(name="nowvideo")
        self.assertIsNotNone(extractor)

        url = "http://www.nowvideo.sx/video/02452e9362f53"

        info = extractor.extract(url)
        self.assertIsInstance(info, dict)

        self.assertIn("id", info.keys())
        self.assertIn("title", info.keys())
        self.assertIn("url", info.keys())
        self.assertIn("ext", info.keys())

    def test_vidbull(self):
        extractor = extractors.get_extractor(name="vidbull")
        self.assertIsNotNone(extractor)

        url = "http://vidbull.com/98acfr8i6pq4.html"
        embed_url = "http://vidbull.com/embed-98acfr8i6pq4.html"

        info = extractor.extract(url)
        self.assertIsInstance(info, dict)

        self.assertIn("id", info.keys())
        self.assertIn("title", info.keys())
        self.assertIn("url", info.keys())
        self.assertIn("ext", info.keys())

    def test_movreel(self):
        extractor = extractors.get_extractor(name="movreel")
        self.assertIsNotNone(extractor)

        url = "http://movreel.com/dpqrm3is53y1"
        embed_url = "http://movreel.com/embed/dpqrm3is53y1"

        info = extractor.extract(url)
        self.assertIsInstance(info, dict)

        self.assertIn("id", info.keys())
        self.assertIn("title", info.keys())
        self.assertIn("url", info.keys())
        self.assertIn("ext", info.keys())

    def test_gorillavid(self):
        pass

if __name__ == "__main__":
    unittest.main()
