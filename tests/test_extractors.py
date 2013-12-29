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

        url = "http://www.divxstage.eu/video/v7f6bhbgvcbgw"
        dlurl = extractor.extract(url)

        self.assertIsNot(dlurl, None)
        self.assertTrue("flv" in dlurl or "mp4" in dlurl)

    def test_gorillavid(self):
        pass

    def test_putlocker(self):
        url = "http://www.putlocker.com/file/B90D29CBE84B2075"

    def test_nowvideo(self):
        pass

    def test_vidbull(self):
        pass

if __name__ == "__main__":
    unittest.main()
