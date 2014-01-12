import logging
import re

from pyquery import PyQuery

from spycis.compat import *
from spycis.utils import (
    session,
    RequestException,
    guess_type,
    urlparse,
    guess_extension)
from .common import BaseExtractor


class VodlockerExtractor(BaseExtractor):

    def __init__(self):
        super(VodlockerExtractor, self).__init__()
        self.host_list = ("vodlocker.com")
        self.holder_url = "http://www.vodlocker.com/embed-{}-640x360.html"
        self.regex_url = re.compile(
            r"https?://(www\.)?vodlocker.com/(?:embed\-)?(?P<id>\w+)(?:\-\d+x\d+.html)?")
        self.example_urls = ('http://vodlocker.com/embed-pgb2ppcmqbxw-640x360.html',
                             'http://vodlocker.com/pgb2ppcmqbxw')

    def extract(self, video_id_or_url):
        if self.regex_url.match(video_id_or_url):
            video_id = self.regex_url.match(video_id_or_url).group('id')
        else:
            video_id = video_id_or_url
        dest_url = self.holder_url.format(video_id)

        try:
            response = session.get(dest_url, timeout=5)
        except RequestException as e:
            logging.error("{}".format(e))
            return None

        video_url = re.search(
            r'file:\s+"(https?://.*?)"', response.text).group(1)
        video_thumbnail = re.search(
            r'image:\s+"(https?://.*?)"', response.text).group(1)
        try:
            video_duration = re.search(
                r'duration:\s+"(.*?)"', response.text).group(1)
        except:
            video_duration = None

        try:
            video_extension = guess_extension(
                guess_type(urlparse(video_url).path)[0])
            assert(video_extension.startswith('.'))
        except:
            fs = "Couldn't extract video extension: {}".format(video_url)
            logging.error(fs)
            return None

        try:
            res = session.get("http://vodlocker.com/" + video_id, timeout=5)
        except RequestException as e:
            logging.error("{}".format(e))
            return None

        video_title = PyQuery('input[name="fname"]', res.content).val()

        info = {
            "id": video_id,
            "title": video_title,
            "url": video_url,
            "ext": video_extension,

            "duration": video_duration,
            "thumbnail": video_thumbnail,
            "extractor": self.name,
            "webpage_url": dest_url,
        }

        return info
