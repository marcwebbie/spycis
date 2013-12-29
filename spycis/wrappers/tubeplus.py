from pyquery import PyQuery

from .common import BaseWrapper, session


class TubeplusWrapper(BaseWrapper):

    def __init__(self):
        self.site_url = "http://www.tubeplus.me"

    def search(self, query):
        search_result = []

        # films
        search_url = self.site_url + "/search/movies/"
        response = session.get(search_url + query)
        pq = PyQuery(response.content)

        for elem in pq('#main .list_item'):
            media = {}
            media['title'] = pq(elem).find('.right>a>b').text()
            media['url'] = "{}{}".format(self.site_url, pq(elem).find('.right>a').attr('href'))
            media['description'] = pq(elem).find('.right>a').text().replace('\n', ' ')
            media['year'] = pq(elem).find('.frelease').text().split('-')[0]
            media['tags'] = ["film"]
            media['thumbnail'] = "{}{}".format(self.site_url, pq(elem).find('.left img').attr('src'))
            try:
                media['rating'] = eval(pq(elem).find('.rank_value').text())
            except:
                pass
            search_result.append(media)

        # tv shows
        search_url = self.site_url + "/search/tv-shows/"
        response = session.get(search_url + query)
        pq = PyQuery(response.content)

        for elem in pq('#main .list_item'):
            media = {}
            media['title'] = pq(elem).find('.right>a>b').text()
            media['url'] = "{}{}".format(self.site_url, pq(elem).find('.right>a').attr('href'))
            media['description'] = pq(elem).find('.right>a').text().replace('\n', ' ')
            media['year'] = pq(elem).find('.frelease').text().split('-')[0]
            media['tags'] = ["tv-show"]
            media['thumbnail'] = "{}{}".format(self.site_url, pq(elem).find('.left img').attr('src'))
            try:
                media['rating'] = eval(pq(elem).find('.rank_value').text())
            except:
                pass
            search_result.append(media)

        return search_result
