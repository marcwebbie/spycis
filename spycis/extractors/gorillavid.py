import logging
from mimetypes import guess_extension, guess_type
import re

from spycis.compat import *
from spycis.utils import session, urlparse, RequestException
from .common import BaseExtractor


class GorillaVidExtractor(BaseExtractor):

    """ gorillavid extractor
    """

    def __init__(self):
        super(GorillaVidExtractor, self).__init__()
        self.host_list = ("gorillavid", "gorillavid.in")
        self.holder_url = "http://gorillavid.in/embed-{}-650x400.html"
        self.regex_url = re.compile(
            r'https?://(?:www.)?gorillavid.in/(?:embed-)?(?P<id>\w+)(?:\-\d+x\d+)?.html'
        )
        self.example_urls = ("http://gorillavid.in/kdk7i5r1p5ye.html",
                             "http://gorillavid.in/embed-kdk7i5r1p5ye.html",
                             "http://gorillavid.in/embed-kdk7i5r1p5ye-960x480.html")

    def extract(self, video_id_or_url):
        """ Extract raw url from novamov url or video id
        """

        video_id = None
        if self.regex_url.match(video_id_or_url):
            video_id = self.regex_url.match(video_id_or_url).group('id')
        else:
            video_id = video_id_or_url
        dest_url = self.holder_url.format(video_id)

        try:
            response = session.get(dest_url, timeout=3)
        except RequestException as e:
            logging.error("{}".format(e))
            return None

        try:
            video_url = re.search(r"file:(?:\s+)?'(http://.*?)',", response.text).group(1)
            assert(video_url)
        except (AttributeError, AssertionError):
            logging.info('url was not found in response: {}'.format(response.url))
            return None

        try:
            video_extension = guess_extension(guess_type(urlparse(video_url).path)[0])
            assert(video_extension.startswith('.'))
        except:
            logging.error("Couldn't extract video extension from url: {}".format(video_url))
            return None

        video_title = '{}{}'.format(video_id, video_extension)

        try:
            video_thumbnail = re.search(r"image:(?:\s+)?'(http://.*?)',", response.text).group(1)
        except AttributeError:
            logging.debug('Couldnt find video thumbnail url from: {}'.format(response.url))
            pass

        info = {
            "id": video_id,
            "title": video_title,
            "url": video_url,
            "ext": video_extension,

            "thumbnail": video_thumbnail,
            "extractor": self.name,
            "webpage_url": dest_url,
        }
        return info
