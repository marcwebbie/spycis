import logging
from mimetypes import guess_extension, guess_type
import re

from pyquery import PyQuery

from .common import BaseExtractor
from spycis.utils import session, baseconv, RequestException
from spycis.compat import unquote, urlparse


def unpacker(p, a, c, k, e=None, d=None):
    for c in reversed(range(c)):
        if(k[c]):
            p = re.sub(r'\b' + baseconv(c, base=a) + r'\b', k[c], p)
    return p


class VidbullExtractor(BaseExtractor):

    """ vidbull.com extractor"""

    def __init__(self):
        super(VidbullExtractor, self).__init__()
        self.host_list = ("vidbull.com")
        self.holder_url = "http://vidbull.com/{}.html"
        self.holder_embed_url = "http://vidbull.com/embed-{}-640x318.html"
        self.regex_url = re.compile(r'https?://(?:www.)?vidbull\.com/(?:embed-)?(?P<id>\w+)(?:\-\d+x\d+)?.html')
        self.example_urls = ("http://vidbull.com/73dldxrrq0ly.html",
                             "http://vidbull.com/embed-73dldxrrq0ly.html",)

    def extract(self, video_id_or_url):
        """Extract raw info from vidbull stream url"""
        if self.regex_url.match(video_id_or_url):
            video_id = self.regex_url.match(video_id_or_url).group('id')
        else:
            video_id = video_id_or_url
        dest_url = self.holder_url.format(video_id)

        try:
            res = session.get(dest_url, timeout=3)
        except RequestException as e:
            logging.error("{}".format(e))
            return None

        pq = PyQuery(res.content)

        video_title = re.sub(r'Verifying Video Request\s+-\s+', '', pq('h3').text())

        try:
            embed_url = self.holder_embed_url.format(video_id)
            res = session.get(embed_url, timeout=3)
        except RequestException as e:
            logging.error("{}".format(e))
            return None

        pq = PyQuery(res.content)

        packed_javascript = re.sub(r'\\', '', pq('#player_code script:not([src])').text())
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
            logging.error("Couldn't find video url in unpacked javascript".format(video_title))
            return None

        try:
            video_extension = guess_extension(guess_type(urlparse(video_url).path)[0])
        except:
            logging.error("Couldn't extract video extension from url: {}".format(video_url))
            return None

        try:
            video_thumbnail = re.search('image:"(http://.*?)"', clean_javascript).group(1)
        except AttributeError:
            pass

        info = {
            "id": video_id,
            "title": video_title,
            "url": video_url,
            "ext": video_extension,

            "extractor": self.name,
            "thumbnail": video_thumbnail,
            "webpage_url": dest_url,
        }
        return info
