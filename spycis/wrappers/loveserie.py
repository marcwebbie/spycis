from __future__ import unicode_literals, division, print_function

from collections import namedtuple
import logging
import re
from pyquery import PyQuery

from spycis.utils import session, RequestException, urljoin, unquote
from spycis.compat import *
from .common import BaseWrapper, Media, Stream, Episode


class LoveserieWrapper(BaseWrapper):

    def __init__(self):
        self.site_url = "http://www.loveserie.com/"
        self.url_regex = re.compile(r"http://www.loveserie.com/streaming")

    @staticmethod
    def _parse_version(vcode):
        """
        parse version code into tuple of (language, subtitles)
        from version in "VO", "VF", "VOST", VOSTFR", "VOSTF"...
        """
        vcode = vcode.upper()
        VersionCode = namedtuple('VersionCode', 'language subtitles')

        if vcode.startswith('VOS'):
            return VersionCode(language="English", subtitles=["French"])
        elif vcode == 'VO':
            return VersionCode(language="English", subtitles=[])
        elif vcode == 'VF':
            return VersionCode(language="French", subtitles=[])

    def get_available_episodes(self, media_url):
        if not self.is_valid_url(media_url):
            raise ValueError(
                "Not a valid url for this site: {}".format(media_url))
        try:
            res = session.get(media_url)
        except RequestException as e:
            logging.error("{}:error on request".format(e.__name__))
            raise StopIteration()

        pq = PyQuery(res.text)

        season_divs = list(pq(".seasonheader + div").items())
        for season_num, sdiv in enumerate(reversed(season_divs), start=1):
            episode_divs = sdiv('.episodeitem').items()

            for episode_num, epdiv in enumerate(episode_divs, start=1):
                title = epdiv('.episodetitle').text().strip()

                episode = Episode(
                    season=season_num,
                    episode=episode_num,
                    title=title,
                    url=media_url,
                    air_date="Inconnu",
                )
                yield episode

    def get_streams(self, media_url, code):
        if not code:
            raise StopIteration()

        if not self.is_valid_url(media_url):
            raise ValueError(
                "Not a valid url for this site: {}".format(media_url))

        try:
            res = session.get(media_url)
        except RequestException as e:
            logging.error("{}:error on request".format(e.__name__))
            raise StopIteration()

        pq = PyQuery(res.text)
        season, episode = self._parse_episode_code(code)

        for snum, sdiv in enumerate(reversed(list(pq('.seasonheader + div').items())), start=1):
            for epnum, epdiv in enumerate(sdiv('.episodeitem').items(), start=1):
                if snum == season and epnum == episode:
                    for link in epdiv('.linkitem').items():
                        language, subtitles = self._parse_version(link('.italic b:last').text())
                        href = link('.watchbutton:first a').attr('href')
                        try:
                            url = re.search(r'(https?://.*?)&', unquote(href)).group(1)
                        except (AttributeError, TypeError) as e:
                            logging.debug("Couldn't get stream url")
                        else:
                            stream = Stream(
                                url=url,
                                language=language,
                                subtitles=subtitles,
                                hd=False,
                            )
                            yield stream

    def search(self, query):
        search_url = "http://www.loveserie.com/streaming/serie"

        qparams = {'q': query}
        try:
            response = session.get(search_url, params=qparams, timeout=3)
        except RequestException as e:
            logging.error("{}".format(e))
            return None

        pq = PyQuery(response.content)

        media_list = []
        for result in pq('.f_news').items():
            title = result('h2').text()
            url = urljoin(self.site_url, result('h2 a').attr('href'))
            wrapper = self.name
            category = Media.TVSHOW

            media = Media(title, url, wrapper, category)

            media.tags = result('.fi_block li:first').text().split()
            media.description = result('.fi_block li:last').text()
            media.thumbnail = result('a img[src]').attr('src')
            try:
                media.year = re.search(
                    r'\d+',
                    result('.fi_block li:first + li').text()).group()
            except AttributeError:
                logging.debug("Couldn't find media year")
                media.year = None

            media_list.append(media)

        return media_list
