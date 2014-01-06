import logging
import re

from pyquery import PyQuery

from .common import BaseExtractor
from spycis.utils import session, RequestException, guess_type, guess_extension
from spycis.compat import urlparse


class PutlockerExtractor(BaseExtractor):

    def __init__(self):
        super(PutlockerExtractor, self).__init__()
        self.host_list = ["putlocker.com"]
        self.holder_url = "http://www.putlocker.com/embed/{}"
        self.regex_url = re.compile(
            r'(http|https)://(www\.)?(?P<host>putlocker\.(com|ws))/(embed/|file/)(?P<id>[\w]+)')
        self.example_urls = ['http://www.putlocker.com/embed/AF115B1580D9C8F1',
                             'http://www.putlocker.ws/file/AF115B1580D9C8F1']

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

        pq = PyQuery(response.text)
        params = {}
        params['fuck_you'] = pq('form input[name=fuck_you]').attr('value')
        params['confirm'] = pq('form input[name=confirm]').attr('value')
        try:
            # request webpage again as POST with query params to get real video page
            session.headers['Referer'] = dest_url
            real_page_response = session.post(dest_url, data=params, timeout=3)
        except RequestException as e:
            logging.error("{}".format(e))
            return None

        try:
            # get api call parameters
            match = re.search(r'/get_file\.php\?stream=(.+?)\'', real_page_response.text)
            api_params = {'stream': match.group(1)}
        except AttributeError:
            logging.error(":{}:Couldn't build api call for : {}".format(self.name, video_id))
            return None

        try:
            api_url = "http://www.putlocker.com/get_file.php"
            api_response = session.get(api_url, params=api_params, timeout=3)
        except RequestException as e:
            logging.error("{}".format(e))
            return None

        video_title = pq('#file_title').text() if pq('#file_title').text() else 'sans titre'
        pq = PyQuery(api_response.content)
        try:
            video_url = pq('[url]:last').attr('url')
        except AssertionError:
            logging.error("Couldn't extract url from api call: {}".format(api_response.url))
            return None

        try:
            video_extension = guess_extension(guess_type(urlparse(video_url).path)[0])
        except (AttributeError, IndexError):
            logging.error('Couldnt get extension from url: {}'.format(video_url))
            return None

        video_duration = pq('[url]:last').attr('duration')
        video_thumbnail = pq('[type^=image]').attr('url')

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
