# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division, print_function

import logging
import re
from pyquery import PyQuery

from spycis.compat import *
from spycis.utils import session, RequestException
from .common import BaseWrapper, Stream


class FilmesOnlineWrapper(BaseWrapper):

    def __init__(self):
        self.site_url = "http://www.filmesonline2.com/"
        self.url_regex = re.compile(r"(http://www.filmesonline2.com/.*?$)")

    def get_streams(self, media_url, code=None):
        try:
            res = session.get(media_url)
        except RequestException as e:
            logging.error("{}:error on request".format(e.__name__))
            return []
        pq = PyQuery(res.text)

        fstr = "https://docs.google.com/file/d/{}/preview"
        streams = []

        if code:
            [("Legendado", tab.parent()('.tab_container')) if tab('a:contains("Legendado")') else "Dublado" for tab in pq('ul.tabs').items()]

        else:
            for url_id in set(re.findall(r"https://docs.google.com/(?:(?:uc\?id=)|(?:file/d/))(\w+)", res.text)):
                if "Legendado" in pq('.audio-video').text():
                    language = "Original"
                    subtitles = ["Portuguese"]
                elif "Dublado" in pq('.audio-video').text():
                    language = "Portuguese"
                    subtitles = []
                else:
                    language = "Unknown"
                    subtitles = []

                stream = Stream(
                    url=fstr.format(url_id),
                    language=language,
                    subtitles=subtitles,
                    hd=False,
                )
                streams.append(stream)

        return streams

    def search(self, query):
        return None
