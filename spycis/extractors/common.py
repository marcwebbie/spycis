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
        """Information extractors are the classes that, given a URL, extract
        information about the video (or videos) the URL refers to. This
        information includes the real video URL, the video title, author and
        others. The information is stored in a dictionary which is then
        returned.

        The dictionaries must include the following fields:

            id:             Video identifier.
            title:          Video title, unescaped.
            url:            Final video URL.
            ext:            Video filename extension.

        The following fields are optional:

            thumbnail:      Full URL to a video thumbnail image.
            description:    One-line video description.
            uploader:       Full name of the video uploader.
            upload_date:    Video upload date (YYYYMMDD).
            uploader_id:    Nickname or id of the video uploader.
            subtitles:      The subtitle file contents as a dictionary in the format
                            {language: subtitles}.
            duration:       Length of the video in seconds, as an integer.
            webpage_url:    Page url from where video was retrieved

        Unless mentioned otherwise, the fields should be Unicode strings.
        """
        raise NotImplementedError("Method extract not overriden by subclass")

    def is_valid_host(self, host):
        return host in self.host_list

    def is_valid_url(self, url):
        return self.regex_url.match(url)

    def get_id(self, url):
        if self.is_valid_url(url):
            match = re.match(self.regex_url, url)
            if match:
                return match.group('id')

    def get_host(self, url):
        """Return the host address for a given stream site extractor"""
        if self.is_valid_url(url):
            match = re.match(self.regex_url, url)
            if match:
                return match.group('host')
