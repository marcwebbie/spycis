# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division, print_function

import logging
import re
from pyquery import PyQuery

from spycis.decorators import lazyproperty
from spycis.utils import session, urljoin, RequestException
from .common import BaseWrapper, Media, Stream, Episode


class LazyStream(Stream):

    @lazyproperty
    def url(self):
        return 1


class TubeplusWrapper(BaseWrapper):

    def __init__(self):
        self.site_url = "http://www.tubeplus.me"
        self.url_regex = re.compile(r"http\://www\.tubeplus\.me/player/\d+/?(?:.*?)?")

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
            raise StopIteration()

        pq = PyQuery(response.content)

        if code:
            try:
                season, episode = re.match(r's(\w+)e(\w+)', code.lower()).groups()
                season = season.strip('0')
                episode = episode.strip('0')
            except AttributeError:
                sys.stderr.write("ERROR: Malformed code not in format s[SS]e[EE]\n".format(code))
                sys.stderr.flush()
                raise StopIteration()

            season_links_text = ' '.join(pq(a).attr('href') for a in pq('.season'))

            rgx = re.compile(r"%s_%s_(\d+)" % (season, episode))
            try:
                episode_id = rgx.search(season_links_text).group(1)
            except AttributeError:
                sys.stderr.write("Could't find episode with code: {}. "
                                 "Use `-s .` to list all available episodes\n".format(code))
                sys.stderr.flush()
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
                    logging.info("Found stream: {}, from id: {}, host: {}".format(stream_url, video_id, host))
                    yield stream_url
                else:
                    logging.warning("Couldn't build stream url from id: {}, host: {}".format(video_id, host))
            else:
                logging.warning("Couldn't extract stream url from url: {}".format(url))
    '''

    def get_all_streams(self):
        pass

        """
        if code:
            # Go to episode page
            season, episode = self._parse_episode_code(code)
            href = PyQuery(
                'a#s{}e{}'.format(season, episode), res).attr('href')

            try:
                res = session.get(urljoin(self.site_url, href))
            except RequestException as e:
                logging.error("{}:error on request".format(e.__name__))
                return []

        streams = []
        for a in PyQuery('.online>.link>a:first', res.content).items():
            elem = a  # DEBUG
            link_href = re.sub('["\'\s+]', "", a.attr('href'))

            try:
                mobj = re.search(r'\((.*?),(?:.*?),(.*?)\)', link_href)
                video_id, video_host = mobj.groups()
                url = self._build_stream_url(video_id, video_host)
                title = a.text().split('-')[-2].strip()

                stream = Stream(
                    hd=False,
                    language="English",
                    subtitles=[],
                    url=url,
                    title=title,
                )
                streams.append(stream)

            except AttributeError as e:
                logging.error("Couldn't find id and host for url")
            except IndexError as e:
                logging.error("Couldn't find stream title")

        return streams
        """

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
        rgx = re.compile(r'(?P<season>\d+)_(?P<episode>\d+)_(?P<video_id>\d+)_(?P<title>.*?)_(?P<air_date>\d+/\d+/\d+)')
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

        """
        season_divs = reversed(list(pq('.parts').items()))
        for season_num, sdiv in enumerate(season_divs, start=1):

            eplinks = reversed([ep for ep in sdiv('.seasons').items()])
            for episode_num, eplink in enumerate(eplinks, start=1):
                try:
                    episode_title = eplink.text().split('-')[-1].strip()
                except (AttributeError, IndexError):
                    episode_title = "Unknown"

                episode_url = urljoin(self.site_url, eplink.attr('href'))
                episode = Episode(
                    season=season_num,
                    episode=episode_num,
                    title=episode_title,
                    url=episode_url)

                # yield episode
                episodes.append(episode)
        """

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
