import re


class Media(object):
    TVSHOW = "tv-show"
    FILM = "film"
    SONG = "song"

    def __init__(self, title, url, wrapper, category, *args, **kwargs):
        self.title = title
        self.url = url
        self.wrapper = wrapper
        self.category = category

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
        try:
            season, episode = re.match(r's(\w+)e(\w+)', code.lower()).groups()
            season = int(season.strip('0'))
            episode = int(episode.strip('0'))
        except:
            raise ValueError("Not a valid code")

        return season, episode

    @property
    def name(self):
        class_name = self.__class__.__name__.lower().replace('wrapper', '')
        return class_name

    def is_valid_url(self, url):
        return self.url_regex.match(url)

    def get_urls(self, url, code=None):
        """Return generator for player pages
        If code is specified fetch urls from page that match code,
        """
        raise NotImplementedError("Method not overriden by subclass")

    def search(self, query):
        """Search the wrapped site with the given query,
        return of media objects containg media infos matching search results
        """
        raise NotImplementedError("Method not overriden by subclass")
