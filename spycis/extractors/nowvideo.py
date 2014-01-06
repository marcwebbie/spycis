import logging
from mimetypes import guess_extension, guess_type
import re

from .common import BaseExtractor
from spycis.utils import session
from spycis.compat import *


class NowVideoExtractor(BaseExtractor):

    def __init__(self):
        super(NowVideoExtractor, self).__init__()
        self.host_list = ["nowvideo.eu", "nowvideo.ch"]
        self.holder_url = "http://embed.nowvideo.sx/embed.php?v={}"
        self.regex_url = re.compile(
            r'http(s)?\://(embed\.|www\.)?(?P<host>nowvideo\.(ws|sx|ch))/((embed\.php\?v\=)|(video/))(?P<id>\w+)'
        )
        self.example_urls = ["http://www.nowvideo.ws/video/12e4587e327fa",
                             "http://embed.nowvideo.sx/embed.php?v=hanu11wjzx2d7"]

    def extract(self, video_id_or_url):
        if self.regex_url.match(video_id_or_url):
            video_id = self.regex_url.match(video_id_or_url).group('id')
        else:
            video_id = video_id_or_url

        # get url
        dest_url = self.holder_url.format(video_id)

        try:
            response = session.get(dest_url, timeout=3)
        except RequestException as e:
            logging.error("{}".format(e))
            return None

        # find params for api call
        query_params = {}
        try:
            match = re.search(r'fkzd=["|\']([\w\s\.\-]+)["|\']', response.text)
            query_params['key'] = match.group(1)
        except:
            logging.error("Couldn't find key param for api call from: {}".format(dest_url))
            return None

        query_params['file'] = video_id
        query_params['cid'] = "undefined"
        query_params['cid2'] = "undefined"
        query_params['cid3'] = "undefined"
        query_params['user'] = "undefined"
        query_params['pass'] = "undefined"

        try:
            # fetch response with raw url
            api_url = "http://www.nowvideo.sx/api/player.api.php"
            api_response = session.get(api_url, params=query_params, timeout=3)
        except RequestException as e:
            logging.error("{}".format(e))
            return None

        try:
            api_regex = re.compile(r'url=(?P<raw_url>.*?)(?:&title=)(?P<title>.*?)%')
            api_dict = api_regex.search(api_response.text).groupdict()
            video_url, video_title = unquote(api_dict["raw_url"]), unquote(api_dict["title"])
            assert(video_url)
        except (AttributeError, AssertionError):
            logging.info('url was not found in response: {}'.format(api_response.url))
            return None

        # Get file extension
        try:
            video_extension = guess_extension(guess_type(urlparse(video_url).path)[0])
        except (AttributeError, IndexError):
            logging.error('Couldnt get extension from url: {}'.format(video_url))
            return None

        info = {
            "id": video_id,
            "title": video_title,
            "url": video_url,
            "ext": video_extension,

            "extractor": self.name,
            "webpage_url": dest_url,
        }
        return info
