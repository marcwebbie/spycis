import re


class BaseExtractor(object):

    def __init__(self):
        self.regex_url = None
        self.host_list = None
        self.holder_url = None
        self.example_urls = None

    @property
    def name(self):
        class_name = self.__class__.__name__.lower().replace('extractor', '')
        return class_name

    def __str__(self):
        return "{0}(name={1}, host_list={2})".format(
            self.__class__.__name__,
            self.name,
            self.host_list
        )

    def extract(self, video_id_or_url):
        pass

    def is_valid_host(self, host):
        return host in self.host_list

    def is_valid_url(self, url):
        return re.match(self.regex_url, url)

    def get_id(self, url):
        if self.is_valid_url(url):
            match = re.match(self.regex_url, url)
            if match:
                return match.group('id')

    def get_host(self, url):
        if self.is_valid_url(url):
            match = re.match(self.regex_url, url)
            if match:
                return match.group('host')
