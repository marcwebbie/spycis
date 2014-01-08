# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division, print_function

import logging
import re
from pyquery import PyQuery

from spycis.utils import session, urljoin, RequestException
from .common import BaseWrapper, Media, Stream, Episode


class TubeplusWrapper(BaseWrapper):

    def __init__(self):
        self.site_url = "http://www.tubeplus.me"
        self.url_regex = re.compile(
            r"http\://www\.tubeplus\.me/player/\d+/?(?:.*?)?")

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

    def get_all_streams(self):
        pass

    def get_available_episodes(self, media_url):
        if not self.is_valid_url(media_url):
            raise ValueError(
                "Not a valid url for this site: {}".format(media_url))

        try:
            res = session.get(media_url)
        except RequestException as e:
            logging.error("{}:error on request".format(e.__name__))
            return []

        episodes = []
        rgx = re.compile(r'(?P<season>\d+)_(?P<episode>\d+)_'
                         '(?P<video_id>\d+)_(?P<title>.*?)_'
                         '(?P<air_date>\d+/\d+/\d+)')
        for mobj in rgx.finditer(res.text):
            episode = Episode(
                season=int(mobj.group('season')),
                episode=int(mobj.group('episode')),
                title=mobj.group('title'),
                url=urljoin(self.site_url,
                            "/player/{}/".format(mobj.group('video_id'))),
                air_date=mobj.group('air_date'),
            )
            episodes.append(episode)

        return sorted(set(episodes))

    def get_streams(self, media_url, code=None):
        if not self.is_valid_url(media_url):
            raise ValueError(
                "Not a valid url for this site: {}".format(media_url))

        if code:
            episodes = list(self.get_available_episodes(media_url))
            season, episode = self._parse_episode_code(code)
            episode = next(
                (e for e in episodes
                 if e.season == season and e.episode == episode),
                None)

            try:
                media_url = episode.url
            except AttributeError:
                logging.warning("Couldn't get episode for code: %s" % code)

        try:
            res = session.get(media_url)
        except RequestException as e:
            logging.error("{}:error on request".format(e.__name__))
            return []

        streams = []
        for a in PyQuery('.online>.link>a:first', res.content).items():
            link_href = re.sub('["\'\s+]', "", a.attr('href'))

            try:
                mobj = re.search(r'\((.*?),(?:.*?),(.*?)\)', link_href)
                video_id, video_host = mobj.groups()
            except AttributeError as e:
                logging.error("Couldn't find id and host for url")
            except IndexError as e:
                logging.error("Couldn't find stream title")
            else:
                url = self._build_stream_url(video_id, video_host)
                if url:
                    stream = Stream(
                        url=url,
                        language="English",
                        subtitles=[],
                        hd=False,
                    )
                    streams.append(stream)

        return streams

    def _search_tv_shows(self, query):
        logging.debug('Searching tv-shows: {}'.format(query))

        search_result = []

        search_url = self.site_url + "/search/tv-shows/"
        response = session.get(search_url + query)
        pq = PyQuery(response.content)

        for elem in pq('#main .list_item').items():
            title = elem('.right>a>b').text()
            video_id = elem('.stitle').attr('id').replace('title_', '')
            url = urljoin(self.site_url, '/player/{}/'.format(video_id))
            wrapper = self.name
            category = Media.TVSHOW

            media = Media(title, url, wrapper, category)

            media.description = elem('.right>a').text().replace('\n', ' ')
            try:
                media.year = elem('.frelease').text().split('-')[0]
            except:
                media.year = None
            media.tags = [category]
            media.thumbnail = "{}{}".format(
                self.site_url, elem('.left img').attr('src'))
            try:
                media.rating = eval(elem('.rank_value').text())
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

        for elem in pq('#main .list_item').items():
            title = elem('.right>a>b').text()
            video_id = elem('.stitle').attr('id').replace('title_', '')
            url = urljoin(self.site_url, '/player/{}/'.format(video_id))
            wrapper = self.name
            category = Media.FILM

            media = Media(title, url, wrapper, category)

            media.description = elem('.right>a').text().replace('\n', ' ')
            try:
                media.year = elem('.frelease').text().split('-')[0]
            except:
                media.year = None
            media.tags = [category]
            media.thumbnail = "{}{}".format(
                self.site_url, elem('.left img').attr('src'))
            try:
                media.rating = eval(elem('.rank_value').text())
            except:
                pass

            search_result.append(media)

        return search_result

    def search(self, query):
        return self._search_tv_shows(query) + self._search_films(query)
