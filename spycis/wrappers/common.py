
class BaseWrapper(object):

    def __init__(self):
        self.site_url = None

    @property
    def name(self):
        class_name = self.__class__.__name__.lower().replace('wrapper', '')
        return class_name

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
            return "http://embed.nowvideo.sx/embed.php?v={}"
        else:
            return None

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
