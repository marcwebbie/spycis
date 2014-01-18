from __future__ import unicode_literals, division, print_function

import logging
import re
from pyquery import PyQuery

from spycis.utils import session, RequestException, urljoin, unquote
from spycis.compat import *
from .common import BaseWrapper, Media, Stream


class VodlockerWrapper(BaseWrapper):

    def __init__(self):
        super(VodlockerWrapper, self).__init__()
        self.site_url = "#"
        self.url_regex = re.compile(r"#")

    def get_streams(self, media_url, code):
        yield Stream(
            url=media_url,
            language="unknown",
            subtitles=[],
            hd=False,
        )

    def search(self, query):
        search_url = "http://vodlocker.com/"

        qparams = {
            "op": "search",
            "k": query,
            "user": None,
            "cat_id": None,
        }

        try:
            response = session.get(search_url, params=qparams, timeout=10)
        except RequestException as e:
            logging.error("{}".format(e))
            return None

        pq = PyQuery(response.content)

        media_list = []
        for tr in pq('.vlist tr').items():
            wrapper = self.name
            title = tr('.link').text()
            url = tr('.link a').attr('href')
            category_info = tr('div:contains("Category")').text()
            category = (
                Media.FILM
                if "Movie" in category_info
                else Media.TVSHOW if "TV" in category_info
                else "None")
            duration = tr('td:first span').text()
            thumbnail = tr('td:first a').attr('style').replace(
                'background-image:url(', '').replace(');', '')
            description = tr('.descr').text()

            media = Media(title=title,
                          url=url,
                          wrapper=wrapper,
                          category=category,
                          duration=duration,
                          thumbnail=thumbnail,
                          description=description)

            media_list.append(media)

        return media_list
