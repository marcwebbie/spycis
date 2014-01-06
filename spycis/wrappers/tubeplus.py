import logging
import re
from pyquery import PyQuery

from spycis.utils import session
from .common import BaseWrapper, Media


class TubeplusWrapper(BaseWrapper):

    def __init__(self):
        self.site_url = "http://www.tubeplus.me"
        self.url_regex = re.compile(r"http\://www\.tubeplus\.me/player/\d+")

    def _build_stream_url(self, video_id, host):
        if host in ("putlocker.com",):
            return "http://www.putlocker.com/embed/{}".format(video_id)
        elif host in ("gorillavid", "gorillavid.in", "gorillavid.com"):
            return "http://gorillavid.in/embed-{}-650x400.html".format(video_id)
        elif host in ("divxstage.eu",):
            return "http://www.divxstage.eu/video/{}".format(video_id)
        elif host in ("vidbull.com",):
            return "http://vidbull.com/embed-{}-650x328.html".format(video_id)
        elif host in ("nowvideo.eu", "nowvideo.ch",):
            return "http://embed.nowvideo.sx/embed.php?v={}".format(video_id)
        elif host in ("movreel.com"):
            return "http://movreel.com/embed/{}".format(video_id)
        elif host in ("novamov.com"):
            return "http://embed.novamov.com/embed.php?v={}".format(video_id)
        elif host in ("divxden.com", "vidxden.com"):
            return "http://www.vidxden.com/embed-{}.html".format(video_id)
        elif host in ("vidbux.com"):
            return "http://www.vidbux.com/embed-{}.html".format(video_id)
        elif host in ("180upload.com", "180upload.nl"):
            return "http://180upload.com/embed-{}.html".format(video_id)
        elif host in ("sockshare.com"):
            return "http://www.sockshare.com/embed/{}".format(video_id)
        elif host in ("novamov.com"):
            return "http://embed.novamov.com/embed.php?v={}".format(video_id)
        else:
            return None

    def get_urls(self, url, code=None):
        """Return generator with stream urls for a given url"""
        if not url.startswith('http://www.tubeplus.me'):
            url = self.site_url + url
        response = session.get(url)
        pq = PyQuery(response.content)

        if code:
            try:
                season, episode = re.match(r's(\w+)e(\w+)', code.lower()).groups()
                season = season.strip('0')
                episode = episode.strip('0')
            except AttributeError:
                logging.warning("Malformed code not in format s[SS]e[EE]".format(code))
                raise StopIteration()

            season_links_text = ' '.join(pq(a).attr('href') for a in pq('.season'))

            rgx = re.compile(r"%s_%s_(\d+)" % (season, episode))
            try:
                episode_id = rgx.search(season_links_text).group(1)
            except AttributeError:
                logging.debug("Could't find episode with this code: {}".format(code))
                raise StopIteration()

            episode_url = self.site_url + '/player/{}/'.format(episode_id)
            response = session.get(episode_url)
            pq = PyQuery(response.content)

        for link in (pq(href).attr('href') for href in pq('.link>a[href^="javascript:show"]')):
            match = re.search(r'\((.*?),(.*?),(.*?)\)', link.replace(' ', ''))
            if match:
                video_id = match.group(1).strip("'\"")
                host = match.group(3).strip("'\"")
                stream_url = self._build_stream_url(video_id, host)
                if stream_url:
                    logging.info("Built stream url: {}, from id: {}, host: {}, link: {}".format(stream_url, video_id, host, link))
                    yield stream_url
                else:
                    logging.warning("Couldn't build stream url from id: {}, host: {}".format(video_id, host))
            else:
                logging.warning("Couldn't extract stream url from url: {}".format(url))

    def _search_tv_shows(self, query):
        logging.debug('Searching tv-shows: {}'.format(query))

        search_result = []

        search_url = self.site_url + "/search/tv-shows/"
        response = session.get(search_url + query)
        pq = PyQuery(response.content)

        for elem in pq('#main .list_item'):
            title = pq(elem).find('.right>a>b').text()
            url = "{}{}".format(self.site_url, pq(elem).find('.right>a').attr('href'))
            wrapper = self.name
            category = Media.TVSHOW

            media = Media(title, url, wrapper, category)

            media.description = pq(elem).find('.right>a').text().replace('\n', ' ')
            media.year = pq(elem).find('.frelease').text().split('-')[0]
            media.tags = ["tv-show"]
            media.thumbnail = "{}{}".format(self.site_url, pq(elem).find('.left img').attr('src'))
            try:
                media.rating = eval(pq(elem).find('.rank_value').text())
            except:
                pass

            search_result.append(media)

        return search_result

    def _search_films(self, query):
        logging.debug('Searching tv-shows: {}'.format(query))

        search_result = []

        search_url = self.site_url + "/search/movies/"
        response = session.get(search_url + query)
        pq = PyQuery(response.content)

        for elem in pq('#main .list_item'):
            title = pq(elem).find('.right>a>b').text()
            url = "{}{}".format(self.site_url, pq(elem).find('.right>a').attr('href'))
            wrapper = self.name
            category = Media.FILM

            media = Media(title, url, wrapper, category)

            media.description = pq(elem).find('.right>a').text().replace('\n', ' ')
            media.year = pq(elem).find('.frelease').text().split('-')[0]
            media.tags = [category]
            media.thumbnail = "{}{}".format(self.site_url, pq(elem).find('.left img').attr('src'))
            try:
                media.rating = eval(pq(elem).find('.rank_value').text())
            except:
                pass

            search_result.append(media)

        return search_result

    def search(self, query):
        return self._search_tv_shows(query) + self._search_films(query)
