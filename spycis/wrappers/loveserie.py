import logging
import re
from pyquery import PyQuery

from spycis.utils import session, RequestException
from spycis.compat import urljoin, unquote
from .common import BaseWrapper, Media


class LoveserieWrapper(BaseWrapper):

    def __init__(self):
        self.site_url = "http://www.loveserie.com/"
        self.url_regex = re.compile(r"http://www.loveserie.com/streaming")

    def get_urls(self, url, code=None):
        try:
            response = session.get(url, timeout=3)
        except RequestException as e:
            logging.error("{}".format(e))
            raise StopIteration()
            # return None

        try:
            season, episode = self._parse_episode_code(code)
        except ValueError:
            logging.warning("Malformed code not in format s[SS]e[EE]".format(code))
            raise StopIteration()
            # return None

        season_id = "#season{}".format(season)
        episode_title = "Episode {}".format(episode)
        pq = PyQuery(response.content)

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
                yield stream_url
            except AttributeError:
                logging.error('Couldnt build stream url from link: {}'.format(link))

        # return stream_urls

    def search(self, query):
        search_url = "http://www.loveserie.com/streaming/serie"

        query_params = {'q': query}
        try:
            response = session.get(search_url, params=query_params, timeout=3)
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
                media.year = re.search(r'\d+', result('.fi_block li:first + li').text()).group()
            except AttributeError:
                media.year = None

            media_list.append(media)

        return media_list
