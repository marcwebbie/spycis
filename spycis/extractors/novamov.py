import logging
from mimetypes import guess_extension, guess_type
import re

from pyquery import PyQuery

from .common import BaseExtractor
from spycis.utils import session, baseconv, urlparse, unquote


class NovamovExtractor(BaseExtractor):

    """novamov.com extractor"""

    def __init__(self):
        super(NovamovExtractor, self).__init__()
        self.host_list = ("novamov.com")
        self.holder_url = "http://embed.novamov.com/embed.php?v={}"
        self.regex_url = re.compile(r"https?://(?:(?:www)|(?:embed))?\.novamov.com/(?:(?:video/)|(?:embed\.php\?v\=))(?P<id>\w+)")
        self.example_urls = ("http://embed.novamov.com/embed.php?v=db14as9rj1kwa",
                             "http://www.novamov.com/video/db14as9rj1kwa")

    def extract(self, video_id_or_url):
        """ Extract raw url from novamov url or video id

        Method to find raw url
            wireshark to find api call
        """
        video_extractor = self.name
        if self.regex_url.match(video_id_or_url):
            video_id = self.regex_url.match(video_id_or_url).group('id')
        else:
            video_id = video_id_or_url
            logging.warning("id was passed to extract in place of url: {}".format(video_id))
        dest_url = self.holder_url.format(video_id)

        try:
            response = session.get(dest_url)
        except:
            logging.error('Error trying to request page at url: {}'.format(dest_url))
            return None

        pq = PyQuery(response.content)

        api_query_params = {}
        try:
            match = re.search(r'flashvars.filekey=["|\']([\w\s\.\-]+)["|\']', response.text)
            api_query_params['key'] = match.group(1)
        except:
            logging.error("Couldn't find key param for api call from: {}".format(dest_url))
            return None
        api_query_params['file'] = video_id
        api_query_params['numOfErrors'] = 0
        api_query_params['cid'] = "undefined"
        api_query_params['cid2'] = "undefined"
        api_query_params['cid3'] = "undefined"
        api_query_params['user'] = "undefined"
        api_query_params['pass'] = "undefined"

        try:
            api_url = "http://www.novamov.com/api/player.api.php"
            api_response = session.post(api_url, params=api_query_params, timeout=5)
        except:
            logging.error('Error trying to request page at url: {}'.format(api_url))
            return None

        try:
            api_regex = re.compile(r'url=(?P<raw_url>.*?)(?:&title=)(?P<title>.*?)%')
            api_dict = api_regex.search(api_response.text).groupdict()
            video_url, video_title = unquote(api_dict["raw_url"]), unquote(api_dict["title"])
            assert(video_title)
            assert(video_url)
        except (AttributeError, AssertionError):
            logging.error("Couldn't extract raw url or title from api response: {}".format(api_response))

        try:
            video_extension = guess_extension(guess_type(urlparse(video_url).path)[0])
        except:
            logging.error("Couldn't extract video extension from url: {}".format(video_url))
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
