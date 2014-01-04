
class BaseWrapper(object):

    def __init__(self):
        self.site_url = None

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
        return of dicts containg media infos matching search results

        Expected keys
            title
            url
        Optional keys:
            description # long description as string
            thumbnail # url to thumbail image
            tags # should be a list
            rating # should be double
            year

        example:
            {'title': 'TPB AFK', 
             'url': 'http://www.example.com/films/tpb-afk/'}
        """
        raise NotImplementedError("Method not overriden by subclass")
