import logging
import re

from .common import BaseExtractor
from spycis.utils import session


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
        video_id = None
        if self.regex_url.match(video_id_or_url):
            video_id = self.regex_url.match(video_id_or_url).group('id')
        else:
            video_id = video_id_or_url

        info = {}

        # get id
        info['id'] = video_id

        # get url
        dest_url = self.holder_url.format(video_id)
        logging.info("Destination url {}".format(dest_url))

        response = session.get(dest_url)

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

        # fetch response with containing raw url
        api_url = "http://www.nowvideo.sx/api/player.api.php"
        api_response = session.get(api_url, params=query_params)

        try:
            match = re.match(r'url=(http://.*?(?:\.flv|\.mp4|\.avi|\.mkv))&', api_response.text)
            url_found = match.group(1)
        except (IndexError, AttributeError):
            logging.info('url was not found in response: {}'.format(api_response.url))
            return None

        info['url'] = url_found

        # Get file extension
        info['ext'] = info['url'].split('.')[-1]

        # get title
        try:
            info['title'] = re.search(r'title=(.*?)(?:&|%)', api_response.text).group(1)
        except:
            logging.warn('Couldnt get title from url: {}'.format(api_response.url))
            return None

        return info
