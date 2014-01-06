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

        url = "http://vidbull.com/73dldxrrq0ly.html"
        embed_url = "http://vidbull.com/embed-73dldxrrq0ly.html"

        info = extractor.extract(embed_url)
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

    def test_novamov(self):
        extractor = extractors.get_extractor(name="novamov")
        self.assertIsNotNone(extractor)

        url = None
        embed_url = "http://embed.novamov.com/embed.php?v=d9f40865e7243"

        info = extractor.extract(embed_url)
        self.assertIsInstance(info, dict)

        self.assertIn("id", info.keys())
        self.assertIn("title", info.keys())
        self.assertIn("url", info.keys())
        self.assertIn("ext", info.keys())

    def test_gorillavid(self):
        extractor = extractors.get_extractor(name="gorillavid")
        self.assertIsNotNone(extractor)

        url = "http://gorillavid.in/kdk7i5r1p5ye.html"
        embed_url = "http://gorillavid.in/embed-kdk7i5r1p5ye.html"

        info = extractor.extract(embed_url)
        self.assertIsInstance(info, dict)

        self.assertIn("id", info.keys())
        self.assertIn("title", info.keys())
        self.assertIn("url", info.keys())
        self.assertIn("ext", info.keys())

    def test_youwatch(self):
        extractor = extractors.get_extractor(name="youwatch")
        self.assertIsNotNone(extractor)

        url = "http://youwatch.org/u44k6agz7l2w"

        info = extractor.extract(url)
        self.assertIsInstance(info, dict)

        self.assertIn("id", info.keys())
        self.assertIn("title", info.keys())
        self.assertIn("url", info.keys())
        self.assertIn("ext", info.keys())

    def test_sockshare(self):
        pass
        # extractor = extractors.get_extractor(name="sockshare")
        # self.assertIsNotNone(extractor)

        # url = None
        # embed_url = "http://www.sockshare.com/embed/54191E3B7033E7D2"

        # info = extractor.extract(embed_url)
        # self.assertIsInstance(info, dict)

        # self.assertIn("id", info.keys())
        # self.assertIn("title", info.keys())
        # self.assertIn("url", info.keys())
        # self.assertIn("ext", info.keys())
if __name__ == "__main__":
    unittest.main()
