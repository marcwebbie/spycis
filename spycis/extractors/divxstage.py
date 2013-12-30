import logging
import re

from .common import BaseExtractor
from spycis.utils import session


class DivxStageExtractor(BaseExtractor):

    """ divxstage extractor
    """

    def __init__(self):
        super(DivxStageExtractor, self).__init__()
        self.host_list = ["divxstage.eu"]
        self.holder_url = "http://www.divxstage.eu/video/{}"
        self.regex_url = re.compile(
            r"(http|https)://(www|embed)\.(?P<host>divxstage\.eu)/(embed\.php\?v=http://www\.divxstage\.eu/)?(file/|video/)(?P<id>\w+$|\w+)(.*?$)"
        )
        self.example_urls = [
            "http://www.divxstage.eu/video/v7f6bhbgvcbgw",
            "http://embed.divxstage.eu/embed.php?v=v7f6bhbgvcbgw"
        ]

    def extract(self, video_id_or_url):
        video_id = None
        if self.regex_url.match(video_id_or_url):
            video_id = self.regex_url.match(video_id_or_url).group('id')
        else:
            video_id = video_id_or_url
        dest_url = self.holder_url.format(video_id)

        info = {}

        logging.info("Destination url {}".format(dest_url))
        response = session.get(dest_url)

        try:
            param_file = re.search(r'flashvars.file=[\'\"](.*?)[\'\"]', response.text).group(1)
            param_filekey = re.search(r'flashvars.filekey=[\'\"](.*?)[\'\"]', response.text).group(1)
            param_cid = re.search(r'flashvars.cid=[\'\"](.*?)[\'\"]', response.text).group(1)
        except AttributeError:
            logging.error("Couldn't match flashvars from url: {}".format(dest_url))
            return None

        query_params = {
            'file': param_file,
            'key': param_filekey,
            'numOfErrors': 0,
            'cid': param_cid,
            'cid2': 'undefined',
            'cid3': 'undefined',
            'pass': 'undefined',
            'user': 'undefined',
        }

        api_url = "http://www.divxstage.eu/api/player.api.php"
        api_response = session.get(api_url, params=query_params)

        try:
            rgx = re.compile(r'url=(http://[\w\.\-/=]+\.flv|mp4|avi|mkv|m4a)')
            url_found = rgx.search(api_response.text).group(1)
        except AttributeError:
            logging.warning("Couldn't file raw url in api call url : {}".format(api_url))
            return None

        info['url'] = url_found
        return info
