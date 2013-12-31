import logging
from mimetypes import guess_extension, guess_type
import re

from pyquery import PyQuery

from .common import BaseExtractor
from spycis.utils import session, baseconv


class VidbullExtractor(BaseExtractor):

    """ vidbull.com extractor"""

    def __init__(self):
        super(VidbullExtractor, self).__init__()
        self.host_list = ["vidbull.com"]
        self.holder_url = "http://vidbull.com/embed-{}-800x600.html"
        self.regex_url = re.compile(r'https?://(?:www.)?vidbull\.com/(?:embed\-)?(?P<id>\w+?)(?:\-\d+x\d+)?\.html')
        self.example_urls = ["http://vidbull.com/98acfr8i6pq4.html",
                             "http://vidbull.com/embed-98acfr8i6pq4-650x328.html",
                             "http://vidbull.com/embed-hkvelwsmgsm0-650x328.html"]

    def extract(self, video_id_or_url):
        """Extract info from stream url"""
        info = {}

        info['extractor'] = self.name

        if self.regex_url.match(video_id_or_url):
            info['id'] = self.regex_url.match(video_id_or_url).group('id')
        else:
            info['id'] = video_id_or_url
        dest_url = self.holder_url.format(info['id'])

        # Get file url
        try:
            response = session.get(dest_url)
        except:
            logging.error('Error trying to request page at url: {}'.format(dest_url))

        pq = PyQuery(response.content)

        javascript = pq('script:contains("eval")').text()
        try:
            param_list = re.search(r"'([\w\|]*jwplayer)'.split", javascript).group(1)
            param_list = param_list.split('|')

            # file url is obfuscated using base 36 convertions
            file_symbol_index = param_list.index('file')
            file_symbol_letter = baseconv(int(file_symbol_index), base=36)
            regex_file_url = '\\{{{0}:"(.*?)",'.format(file_symbol_letter)
            obfuscated_file_url = re.search(regex_file_url, javascript).group(1)

            # deobfuscate url
            real_file_url = re.sub(
                r'\w+',
                lambda x: str(param_list[int(x.group(), 36)] if param_list[int(x.group(), 36)] else x.group()),
                obfuscated_file_url
            )
            info['url'] = real_file_url
        except (AttributeError, ValueError):
            logging.debug("Couldn't parse obfuscated javascript: {}".format(pq('span').text()))
            return None

        # Get file extension
        try:
            info['ext'] = guess_extension(guess_type(info['url'])[0]).strip('.')
        except (AttributeError, IndexError):
            logging.error('Couldnt get extension from url: {}'.format(info['url']))
            return None

        # Get thumbnail url
        try:
            info['thumbnail'] = re.search(r'http://.*?\.jpg', response.text).group(1)
        except:
            pass

        # Get title
        try:
            response = session.get("http://vidbull.com/{}.html".format(info['id']))
            pq = PyQuery(response.content)
            info['title'] = pq('title').text().replace('VidBull - Watch ', '')
        except:
            logging.warn('Couldnt get title from url: {}'.format(response.url))
            return None

        return info
