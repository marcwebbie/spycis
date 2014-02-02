import re
from collections import namedtuple

from spycis.compat import *

Stream = namedtuple("Stream", "url language subtitles hd")
Episode = namedtuple("Episode", "season episode title url air_date")


class Media(object):
    TVSHOW = "tv-show"
    FILM = "film"
    SONG = "song"

    def __init__(self, title, url, wrapper, category, **kwargs):
        self.title = title
        self.url = url
        self.wrapper = wrapper
        self.category = category

        self.duration = kwargs.get("duration", None)
        self.description = kwargs.get("description", None)
        self.thumbnail = kwargs.get("thumbnail", None)
        self.tags = kwargs.get("tags", [])
        self.rating = kwargs.get("rating", None)
        self.year = kwargs.get("year", None)

    def __str__(self):
        return "<Media: {0.title}, {0.category}, {0.wrapper}>".format(self)

    def __repr__(self):
        return self.__str__()


class BaseWrapper(object):

    def __init__(self):
        self.site_url = None

    @staticmethod
    def _parse_episode_code(code):
        """Parse an episode code in the format sSSeEE,
        returns tuple (season_num, episode_num)"""
        try:
            season, episode = re.match(r'[sS]?(\d+)[eE](\d+)', code.lower()).groups()
            season = int(season.lstrip('0'))
            episode = int(episode.lstrip('0'))
        except AttributeError:
            raise ValueError("ERROR: Malformed code not in format s[SS]e[EE]\n")
        return season, episode

    @property
    def name(self):
        class_name = self.__class__.__name__.lower().replace('wrapper', '')
        return class_name

    def is_valid_url(self, url):
        return self.url_regex.match(url)

    def get_streams(self, url, code=None):
        """Return generator for player pages
        If code is specified fetch urls from page that match code,
        """
        raise NotImplementedError("Method not overriden by subclass")

    def search(self, query):
        """Search the wrapped site with the given query,
        return of media objects containg media infos matching search results
        """
        raise NotImplementedError("Method not overriden by subclass")
