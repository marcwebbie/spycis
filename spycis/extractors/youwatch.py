import logging
from mimetypes import guess_extension, guess_type
import re

from pyquery import PyQuery

from .common import BaseExtractor
from spycis.utils import session, urlparse, RequestException, unquote, unpacker


class YouWatchExtractor(BaseExtractor):

    """ youwatch.org extractor"""

    def __init__(self):
        super(YouWatchExtractor, self).__init__()
        self.host_list = ["youwatch.org"]
        self.holder_url = "http://youwatch.org/{}"
        self.holder_embed_url = "http://youwatch.org/embed-{}-640x360.html"
        self.regex_url = re.compile(r'https?://(?:www.)?youwatch.org/(?:embed-)?(?P<id>\w+)(?:\-\d+x\d+)?')
        self.example_urls = ("http://youwatch.org/u44k6agz7l2w", "http://youwatch.org/embed-u44k6agz7l2w-640x360.html")

    def extract(self, video_id_or_url):
        """Extract info from a youwatch.org stream url"""
        if self.regex_url.match(video_id_or_url):
            video_id = self.regex_url.match(video_id_or_url).group('id')
        else:
            video_id = video_id_or_url
        dest_url = self.holder_url.format(video_id)

        try:
            res = session.get(self.holder_embed_url.format(video_id), timeout=3)
        except RequestException as e:
            logging.error("{}".format(e))
            return None

        pq = PyQuery(res.content)

        packed_javascript = re.sub(r'\\', '', pq('script:contains("eval")').text())
        rgx = re.compile(r"}\('(.+)',(\d+),(\d+),'([\w|]+)'")
        try:
            parg1 = re.search(rgx, packed_javascript).group(1)
            parg2 = int(re.search(rgx, packed_javascript).group(2))
            parg3 = int(re.search(rgx, packed_javascript).group(3))
            parg4 = re.search(rgx, packed_javascript).group(4).split('|')
            clean_javascript = unquote(unpacker(parg1, parg2, parg3, parg4))
        except:
            logging.debug("Couldn't parse obfuscated javascript: {}".format(pq('span').text()))
            return None

        try:
            video_url = re.search('file:"(http://.*?)"', clean_javascript).group(1)
        except AttributeError:
            logging.error("Couldn't find video url in unpacked javascript")
            return None

        try:
            video_extension = guess_extension(guess_type(urlparse(video_url).path)[0])
        except:
            logging.error("Couldn't extract video extension from url: {}".format(video_url))
            return None

        try:
            video_title = '.'.join(pq('title').text().split())
            assert(video_title)
        except:
            logging.debug('Couldnt find video title, using generic')
            video_title = "{}{}".format(video_id, video_extension)

        info = {
            "id": video_id,
            "title": video_title,
            "url": video_url,
            "ext": video_extension,

            "extractor": self.name,
            "webpage_url": dest_url,
        }
        return info
