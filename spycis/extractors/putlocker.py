import logging
from mimetypes import guess_extension
import re

from pyquery import PyQuery

from .common import BaseExtractor
from spycis.utils import session


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
        info = {}
        if self.regex_url.match(video_id_or_url):
            info['id'] = self.regex_url.match(video_id_or_url).group('id')
        else:
            info['id'] = video_id_or_url
        dest_url = self.holder_url.format(info['id'])

        try:
            html_embed = session.get(dest_url).text
        except:
            logging.info("Couldn't fetch page at url: {}".format(dest_url))
            return None

        import pdb
        pdb.set_trace()

        # get form params 'fuck_you' and 'confirm'
        pq = PyQuery(html_embed)
        params = {}
        params['fuck_you'] = pq('form input[name=fuck_you]').attr('value')
        params['confirm'] = pq('form input[name=confirm]').attr('value')

        # Get file title
        info['title'] = pq('#file_title').text()

        # request webpage again as POST with query params to get real video page
        session.headers['Referer'] = dest_url
        real_page_response = session.post(dest_url, params)

        try:
            # get api call parameters
            match = re.search(r'/get_file\.php\?stream=(.+?)\'', real_page_response.text)
            api_params = {'stream': match.group(1)}
        except AttributeError:
            logging.error(":{}:Couldn't build api call for : {}".format(self.name, info['id']))
            return None

        api_response = session.get("http://www.putlocker.com/get_file.php", params=api_params)

        pq = PyQuery(api_response.content)
        url_found = pq('[url]:last').attr('url')
        if not url_found:
            logging.warning("Couldn't extract url from api call: {}".format(api_response.url))
            return None

        info['url'] = url_found
        info['duration'] = pq('[url]:last').attr('duration')
        info['thumbnail'] = pq('[type^=image]').attr('url')
        info['ext'] = guess_extension(pq('[url]:last').attr('type'))
        try:
            info['ext'] = info['ext'].strip('.')
        except AttributeError:
            logging.error("Couldn't get extension for file: {}".format(info['url']))
            return None

        return info
