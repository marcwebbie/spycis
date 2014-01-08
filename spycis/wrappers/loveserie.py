from collections import namedtuple
import logging
import re
from pyquery import PyQuery

from spycis.utils import session, RequestException
from spycis.compat import urljoin, unquote
from .common import BaseWrapper, Media, Stream, Episode


class LoveserieWrapper(BaseWrapper):

    def __init__(self):
        self.site_url = "http://www.loveserie.com/"
        self.url_regex = re.compile(r"http://www.loveserie.com/streaming")

    '''
    def get_streams_backup(self, media_url, code=None):
        """Return generator with stream objects found for media_url
        """

        if not self.is_valid_url(media_url):
            raise ValueError("Not a valid url for this site")

        try:
            response = session.get(media_url, timeout=3)
        except RequestException as e:
            logging.error("{}".format(e))
            # raise StopIteration()
            return []

        season, episode = self._parse_episode_code(code)

        season_id = "#season{}".format(season)
        episode_title = "Episode {}".format(episode)
        pq = PyQuery(response.content)

        stream_urls = []
        for eitem in pq(season_id)('.episodeitem').items():
            episode_name = eitem('.episodetitle').text()
            links = []
            for link in eitem('.linkitem').items():
                try:
                    link_version = link('td:first').text().split()[-1]
                    link_href = unquote(link('a:contains("Regarder")').attr('href'))
                    links.append((link_version, link_href,))
                except (IndexError, AttributeError, TypeError):
                    logging.error('Couldnt build link from link_item'.format(link))

            for link in links:
                try:
                    # build stream urls out of link tuples
                    stream_url = re.search(r'(https?://.*?)&', link[1]).group(1)
                    stream_url += "?version={}".format(link[0])
                    # yield stream_url
                    stream_urls.append(stream_url)
                except AttributeError:
                    logging.error('Couldnt build stream url from link: {}'.format(link))

        return stream_urls
    '''

    @staticmethod
    def _parse_version(vcode):
        """
        parse version code into tuple of (language, subtitles)
        from version in "VO", "VF", "VOST", VOSTFR", "VOSTF"...
        """
        vcode = vcode.upper()
        VersionCode = namedtuple('VersionCode', 'language subtitles')
        if vcode.startswith('VO'):
            return VersionCode(language="English", subtitles=[])
        elif vcode.startswith('VF'):
            return VersionCode(language="French", subtitles=[])
        elif vcode.startswith('VOST'):
            return VersionCode(language="English", subtitles=["French"])

    '''
    def get_all_streams(self, media_url):
        if not self.is_valid_url(media_url):
            raise ValueError("Not a valid url for this site")
        try:
            res = session.get(media_url)
        except RequestException as e:
            logging.error("{}:error on request".format(e.__name__))
            raise StopIteration()

        pq = PyQuery(res.text)

        # transverse all seasons
        season_divs = list(pq(".seasonheader + div").items())

        for season_num, sdiv in enumerate(reversed(season_divs), start=1):
            episode_divs = sdiv('.episodeitem').items()

            for episode_num, epdiv in enumerate(episode_divs, start=1):
                title = epdiv('.episodetitle').text().strip()
                version = epdiv('td:first').text().split()[-1]
                language, subtitles = self._parse_version(version)

                links = epdiv('.watchbutton a:contains("Regarder")').items()

                for href in [a.attr('href') for a in links]:
                    try:
                        mobj = re.search(r'(https?://.*?)&', unquote(href))
                        url = mobj.group(1)
                    except (AttributeError, TypeError):
                        logging.error("Couldn't build stream url")
                    else:
                        stream = Stream(
                            url=url,
                            title=title,
                            season=season_num,
                            episode=episode_num,
                            language=language,
                            subtitles=subtitles,
                            air_date="Inconnu",
                            hd=False,)

                        yield stream
    '''

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

        season, episode = self._parse_episode_code(code)

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
                if season_num == season and episode_num == episode:
                    version = epdiv('td:first').text().split()[-1]
                    language, subtitles = self._parse_version(version)

                    links = epdiv('.watchbutton a:contains("Regarder")').items()

                    for href in [a.attr('href') for a in links]:
                        try:
                            mobj = re.search(r'(https?://.*?)&', unquote(href))
                            url = mobj.group(1)
                        except (AttributeError, TypeError):
                            logging.error("Couldn't build stream url")
                        else:
                            stream = Stream(
                                url=url,
                                language=language,
                                subtitles=subtitles,
                                hd=False,)

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
            # --------------
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
