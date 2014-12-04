import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from spycis import extractors
from spycis import wrappers
from spycis import __main__
from spycis.compat import StringIO
from spycis.wrappers.example import ExampleWrapper


class Args(object):

    def __init__(self, query, *args, **kwargs):
        self.query = query

        self.download = kwargs.get("download", None)
        self.play = kwargs.get("play", None)
        self.player = kwargs.get("player", "vlc")
        self.position = kwargs.get("position", 0)
        self.raw_urls = kwargs.get("raw_urls", None)
        self.site = kwargs.get("site", "tubeplus")
        self.stream = kwargs.get("stream", None)
        self.stream_urls = kwargs.get("stream_urls", None)
        self.subtitles = kwargs.get("subtitles", None)
        self.verbose = kwargs.get("verbose", False)
        self.workers = kwargs.get("workers", 8)
        self.version = kwargs.get("version", None)


class WrappersTests(unittest.TestCase):

    def test_get_all_returns_example_wrapper_class(self):
        example_wrapper = ExampleWrapper
        wrapper_list = wrappers.get_all()
        self.assertIn(example_wrapper, wrapper_list)

    def test_get_instances_result_contains_an_example_wrapper_instance(self):
        instance_list = wrappers.get_instances()
        self.assertNotEqual([], [i for i in instance_list if isinstance(i, ExampleWrapper)])

    def test_get_example_wrapper_instance_by_name_returns_valid_instance(self):
        self.assertTrue(isinstance(wrappers.get_instance("example"), ExampleWrapper))

class InterfaceTests(unittest.TestCase):

    """Test the minimal interface that spycis must have
    """

    def setUp(self):
        self.original_stdout = sys.stdout
        self.original_stderr = sys.stderr
        sys.stdout = StringIO()
        sys.stderr = sys.stdout

    def tearDown(self):
        sys.stdout = self.original_stdout
        sys.stderr = self.original_stderr

    def assertContainsRawUrl(self, container):
        valid_formats = (u"mp4", u"flv", u"avi", u"mkv", u"mp3")
        if not any(True for f in valid_formats if f in container):
            self.original_stdout.write(container)
            self.original_stderr.write(container)
        self.assertTrue(any(True for f in valid_formats if f in container))

    def assertContainsStreamUrl(self, container):
        extractor_names = (w.name for w in extractors.get_instances())
        if not any(True for name in extractor_names if name in container):
            self.original_stdout.write(container)
            self.original_stderr.write(container)
        self.assertTrue(any(True for name in extractor_names if name in container))

    def test_basic_search_with_query(self):
        '''spycis mentalist
        '''
        args = Args(query="mentalist")

        __main__.run(args)
        output = sys.stdout.getvalue()

        self.assertIn("Mentalist", output)
        self.assertIn("tv-show", output)
        self.assertIn("film", output)

    def test_basic_search_returns_stream_urls_for_a_media_url(self):
        """spycis http://www.tubeplus.me/player/553643/The_Lion_King/
        """
        query = "http://www.tubeplus.me/player/553643/The_Lion_King/"
        args = Args(query=query)

        __main__.run(args)
        output = sys.stdout.getvalue()

        self.assertContainsStreamUrl(output)

    def test_basic_search_returns_raw_urls_for_stream_url(self):
        """spycis http://www.divxstage.eu/video/46b593256e86d
        """
        query = "http://www.divxstage.eu/video/46b593256e86d"
        args = Args(query=query)

        __main__.run(args)
        output = sys.stdout.getvalue()

        self.assertContainsRawUrl(output)

    def test_search_shortcuts_get_stream_urls_by_episode_code(self):
        '''spycis -s s02e03 "Vampire Diaries"
        '''

        query = "Vampire Diaries"
        episode_code = "s02e03"
        args = Args(query=query, stream_urls=episode_code)

        __main__.run(args)
        output = sys.stdout.getvalue()

        self.assertContainsStreamUrl(output)

    def test_search_shortcuts_get_raw_urls_by_episode_code(self):
        """spycis -r s02e03 "Vampire Diaries"
        """

        query = "Vampire Diaries"
        episode_code = "s02e03"
        args = Args(query=query, raw_urls=episode_code)

        __main__.run(args)
        output = sys.stdout.getvalue()

        self.assertContainsRawUrl(output)

    def test_search_shortcuts_get_stream_urls_by_episode_code_and_position(self):
        """spycis -p 1 -s s01e16 house
        """

        query = "house"
        episode_code = "s01e16"
        position = 2
        args = Args(query=query, position=position, stream_urls=episode_code)

        __main__.run(args)
        output = sys.stdout.getvalue()

        self.assertContainsStreamUrl(output)

    def test_search_shortcuts_get_raw_urls_by_episode_code_and_position(self):
        """spycis -p 1 -r r01e16 house
        """

        query = "house"
        episode_code = "s01e16"
        position = 2
        args = Args(query=query, position=position, raw_urls=episode_code)

        __main__.run(args)
        output = sys.stdout.getvalue()

        self.assertContainsRawUrl(output)

    def test_search_shortcuts_get_raw_urls_by_position_for_films(self):
        """spycis -p 30 "Lion King"
        """

        query = "Lion King"
        args = Args(query=query, position=30)

        __main__.run(args)
        output = sys.stdout.getvalue()

        self.assertContainsRawUrl(output)


if __name__ == "__main__":
    unittest.main()
