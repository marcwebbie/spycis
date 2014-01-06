import logging
from mimetypes import guess_extension, guess_type
import re

from pyquery import PyQuery

from .common import BaseExtractor
from spycis.utils import session, baseconv, urlparse


class MovreelExtractor(BaseExtractor):

    """ movreel.com extractor"""

    def __init__(self):
        super(MovreelExtractor, self).__init__()
        self.host_list = ["movreel.com"]
        self.holder_url = "http://movreel.com/{}"
        self.regex_url = re.compile(r'https?://(?:www.)?movreel\.com/(?:embed/)?(?P<id>\w+)')
        self.example_urls = ["http://movreel.com/embed/dpqrm3is53y1",
                             "http://movreel.com/dpqrm3is53y1"]

    def extract(self, video_id_or_url):
        """Extract info from a movreel.com stream url"""
        video_extractor = self.name
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

        pq = PyQuery(response.content)

        headers = {'Referer': dest_url, 'Origin': 'http://movreel.com'}
        post_data = {elem.attr('name'): elem.val() for elem in pq('form input[name]').items()}
        try:
            # post form_data to the same page to get real file page
            res = session.post(dest_url, data=post_data, headers=headers, timeout=3)
        except RequestException as e:
            logging.error("{}".format(e))
            return None

        pq = PyQuery(res.content)

        video_title = pq('nobr b').text()
        if not video_title:
            video_title = pq('center h3').text().replace(pq('center h3 sup').text(), '').strip()

        video_url = pq('a[href$="{}"]'.format(video_title)).attr('href')
        if not video_url:
            logging.error("Couldn't find video url ending with: {}".format(video_title))
            return None

        try:
            video_extension = guess_extension(guess_type(urlparse(video_url).path)[0])
        except:
            logging.error("Couldn't extract video extension from url: {}".format(video_url))
            return None

        video_thumbnail = pq('#player_img img[src]').attr('src')

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
