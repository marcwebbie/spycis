import re

from .common import BaseExtractor


class ExampleExtractor(BaseExtractor):

    def __init__(self):
        super(ExampleExtractor, self).__init__()
        self.host_list = ["example.com"]
        self.holder_url = "http://www.example.com/{}.html"
        self.regex_url = re.compile(r'https?://(?:www.)?example\.com/(?P<id>.*?)(?:\.html)')
