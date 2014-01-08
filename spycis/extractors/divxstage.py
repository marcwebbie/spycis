import logging
from mimetypes import guess_extension, guess_type
import re

from .common import BaseExtractor
from spycis.utils import session, RequestException
from spycis.compat import *


class DivxStageExtractor(BaseExtractor):

    """ divxstage extractor
    """

    def __init__(self):
        super(DivxStageExtractor, self).__init__()
        self.host_list = ("divxstage.eu")
        self.holder_url = "http://embed.divxstage.eu/embed.php?v={}"
        self.regex_url = re.compile(
            r'https?://((www)|(embed))?\.divxstage\.eu/((video/)|(embed\.php\?v\=))(?P<id>\w+)'
        )
        self.example_urls = (
            "http://www.divxstage.eu/video/v7f6bhbgvcbgw",
            "http://embed.divxstage.eu/embed.php?v=v7f6bhbgvcbgw"
        )

    def extract(self, video_id_or_url):
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

        api_query_params = {}
        try:
            filekey_var = re.search(r'flashvars.filekey=(\w+);', response.text).group(1)
            api_query_params['key'] = re.search(filekey_var + r'="(.*?)";', response.text).group(1)
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

        # fetch response with containing raw url
        api_url = "http://www.divxstage.eu/api/player.api.php"
        try:
            api_response = session.post(api_url, params=api_query_params, timeout=3)
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
