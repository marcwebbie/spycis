import logging
import re

from pyquery import PyQuery
from .common import BaseWrapper, session


class TubeplusWrapper(BaseWrapper):

    def __init__(self):
        self.site_url = "http://www.tubeplus.me"

    def get_urls(self, url):
        """Return generator with stream urls for a given url"""
        if not url.startswith('http://www.tubeplus.me'):
            url = self.site_url + url
        response = session.get(url)
        pq = PyQuery(response.content)

        for link in (pq(href).attr('href') for href in pq('.link>a[href^="javascript:show"]')):
            match = re.search(r'\((.*?),(.*?),(.*?)\)', link.replace(' ', ''))
            if match:
                video_id = match.group(1).strip("'\"")
                host = match.group(3).strip("'\"")
                stream_url = self._build_stream_url(video_id, host)
                if stream_url:
                    yield stream_url
                else:
                    logging.warning("Couldn't build stream url from id: {}, host: {}".format(video_id, host))
            else:
                logging.warning("Couldn't extract stream url from url: {}".format(url))

    def search(self, query):
        search_result = []

        # films
        search_url = self.site_url + "/search/movies/"
        response = session.get(search_url + query)
        pq = PyQuery(response.content)

        for elem in pq('#main .list_item'):
            media = {}
            media['title'] = pq(elem).find('.right>a>b').text()
            media['url'] = "{}{}".format(self.site_url, pq(elem).find('.right>a').attr('href'))
            media['description'] = pq(elem).find('.right>a').text().replace('\n', ' ')
            media['year'] = pq(elem).find('.frelease').text().split('-')[0]
            media['tags'] = ["film"]
            media['thumbnail'] = "{}{}".format(self.site_url, pq(elem).find('.left img').attr('src'))
            try:
                media['rating'] = eval(pq(elem).find('.rank_value').text())
            except:
                pass
            search_result.append(media)

        # tv shows
        search_url = self.site_url + "/search/tv-shows/"
        response = session.get(search_url + query)
        pq = PyQuery(response.content)

        for elem in pq('#main .list_item'):
            media = {}
            media['title'] = pq(elem).find('.right>a>b').text()
            media['url'] = "{}{}".format(self.site_url, pq(elem).find('.right>a').attr('href'))
            media['description'] = pq(elem).find('.right>a').text().replace('\n', ' ')
            media['year'] = pq(elem).find('.frelease').text().split('-')[0]
            media['tags'] = ["tv-show"]
            media['thumbnail'] = "{}{}".format(self.site_url, pq(elem).find('.left img').attr('src'))
            try:
                media['rating'] = eval(pq(elem).find('.rank_value').text())
            except:
                pass
            search_result.append(media)

        return search_result
