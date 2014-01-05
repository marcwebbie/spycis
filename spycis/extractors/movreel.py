import logging
from mimetypes import guess_extension, guess_type
import re

from pyquery import PyQuery

from .common import BaseExtractor
from spycis.utils import session, baseconv


class MovreelExtractor(BaseExtractor):

    """ movreel.com extractor"""

    def __init__(self):
        super(MovreelExtractor, self).__init__()
        self.host_list = ["movreel.com"]
        self.holder_url = "http://movreel.com/embed/{}"
        self.regex_url = re.compile(r'https?://(?:www.)?movreel\.com/(?:embed/)?(?P<id>\w+)')
        self.example_urls = ["http://movreel.com/embed/dpqrm3is53y1",
                             "http://movreel.com/dpqrm3is53y1"]

    def extract(self, video_id_or_url):
        """Extract info from stream url"""

        logging.warning('Extractor for movreel is not yet implemented')
        return None
        # info = {}
        # info['extractor'] = self.name

        # if self.regex_url.match(video_id_or_url):
        #     info['id'] = self.regex_url.match(video_id_or_url).group('id')
        # else:
        #     info['id'] = video_id_or_url
        # dest_url = self.holder_url.format(info['id'])
        # dest_url = "http://movreel.com/embed-dpqrm3is53y1-854x480.html"

        # try:
        #     response = session.get(dest_url)
        # except:
        #     logging.error('Error trying to request page at url: {}'.format(dest_url))
        #     return None

        # pq = PyQuery(response.content)
        # import pdb
        # pdb.set_trace()

        # Post params to the same page to get real file page
        # params = {elem.attr('name'): elem.val() for elem in pq('form input').items()}
        # try:
        #     headers = {'Referer': dest_url, 'Origin': 'http://movreel.com'}
        #     res = session.post(dest_url, params=params, headers=headers)
        # except:
        #     logging.error('Error trying to request page at url: {}'.format(dest_url))
        #     return None

        # return info
