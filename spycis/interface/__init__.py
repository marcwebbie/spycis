import argparse
import logging
import subprocess
import sys
from threading import Thread
import time
try:
    from queue import Queue
except ImportError:
    # fallback to python2
    from Queue import Queue

from spycis import extractors, wrappers
from spycis.utils import session


class LogFormatter(logging.Formatter):
    color = {
        "HEADER": '\033[95m',       # magenta
        "DEBUG": '\033[94m',        # blue
        "INFO": '\033[92m',         # green
        "WARNING": '\033[93m',      # yellow
        "WARN": '\033[93m',         # yellow
        "ERROR": '\033[91m',        # red
        "CRITICAL": '\033[41m',     # background red
        "FATAL": '\033[41m',        # background red
        "ENDC": '\033[0m',          # end formatting
    }

    def format(self, record):
        final_msg = super(LogFormatter, self).format(record)

        level = record.__dict__['levelname']
        return LogFormatter.color[level] + final_msg + LogFormatter.color['ENDC']


def get_args():
    aparser = argparse.ArgumentParser()

    aparser.add_argument("--site", default="tubeplus", help="stream site name (example: --site streamsite)")
    aparser.add_argument("-v", "--verbose", action="store_true", help="verbose output for debugging")
    aparser.add_argument("-w", "--workers", action="store", type=int, default=8, help="number of extraction thread workers")
    aparser.add_argument("-s", "--search", help="search site, prints result, ex: '-s Vampire Diaries'")
    aparser.add_argument("-c", "--code", help="code from episode to download, ex: '-c s01e02'")
    aparser.add_argument("-u", "--url", help="url to get stream urls from")
    aparser.add_argument("-x", "--extract", action="store_true", help="extract raw video urls from stream urls")
    aparser.add_argument("-p", "--play", action="store_true", help="play video using vlc or ffplay")
    aparser.add_argument("-d", "--download", action="store_true", help="play video using vlc or ffplay")
    aparser.add_argument("--print-info", action="store_true", help="print info instead of urls")
    aparser.add_argument("--player", default="cvlc", help="specify the player to use for the --play option, ex: --player vlc")
    args = aparser.parse_args()

    return args


class Reporter(object):

    last_time = time.time()
    last_length = 0
    last_dlrate = "0 K"

    def sizeof_fmt(num):
        for x in ['bytes', 'K', 'M', 'G', 'T', 'P']:
            if num < 1024.0:
                return "%3.1f %s" % (num, x)
            num /= 1024.0

    @staticmethod
    def report(curr_size, total_size):
        if (time.time() - Reporter.last_time) > 1:
            done = int(50 * curr_size / total_size)
            percent = int(curr_size * 100 / total_size)
            bytes = (curr_size - Reporter.last_length) / (time.time() - Reporter.last_time)
            Reporter.last_dlrate = Reporter.sizeof_fmt(bytes)
            Reporter.last_time = time.time()
            Reporter.last_length = curr_size

            report_line = "\r [{0}{1}] {2:>3}% {3:>6}B ({4}/s)    \r".format(
                '=' * done,
                ' ' * (50 - done),
                percent,
                Reporter.sizeof_fmt(total_size),
                Reporter.last_dlrate,
            )
            sys.stdout.write(report_line)
            sys.stdout.flush()


class Downloader(object):

    def __init__(self, workers=None, print_as_info=False, player="cvlc"):
        self.timeout = 5
        self.workers = workers
        self.extraction_queue = Queue()
        self.print_as_info = print_as_info
        self.extractor_list = list(extractors.get_instances())
        self.info_list = []
        self.player = player

    def _extract_worker(self):
        while True:
            url = self.extraction_queue.get()
            logging.debug("init extracting file url from: {}".format(url))

            extractor = next((e for e in self.extractor_list if e.is_valid_url(url)), None)
            if extractor:
                info = extractor.extract(url)
                if info:
                    print(info if self.print_as_info else info['url'])
                    self.info_list.append(info)
            else:
                logging.debug("Couldn't get extractor for url: {0}".format(url))

            self.extraction_queue.task_done()

    def spawn_workers(self):
        for i in range(self.workers):
            worker = Thread(target=self._extract_worker)
            worker.daemon = True
            worker.start()
            logging.debug("started worker: {}".format(i + 1))

    def extract_async(self, stream_urls):
        self.spawn_workers()
        for url in stream_urls:
            self.extraction_queue.put(url)
            logging.debug("Added url to extract queue: {}".format(url))
        return self.extraction_queue.join()

    def extract(self, stream_urls):
        if self.workers > 0:
            return self.extract_async(stream_urls)

        for url in stream_urls:
            extractor = next((e for e in self.extractor_list if e.is_valid_url(url)), None)
            if extractor:
                info = extractor.extract(url)
                if info:
                    print(info if self.print_as_info else info['url'])
                    self.info_list.append(info)

    def play(self):
        info = next((i for i in self.info_list), None)
        if info:
            command = [
                self.player,
                info['url'],
            ]
            subprocess.call(command)

    def download(self):
        try:
            info = next((i for i in self.info_list if i['ext'] in i['title']), self.info_list[0])
        except (TypeError, IndexError):
            logging.debug("Info not found to download")

        response = session.get(info['url'], stream=True)
        total_length = response.headers.get('content-length')

        local_filename = info['title']
        if info['ext'] not in local_filename:
            local_filename = "{}.{}".format(info['title'], info['ext'])

        with open(local_filename, 'wb') as f:
            print("Saving into : {}".format(local_filename))
            if total_length is None:  # no content length header
                f.write(response.content)
            else:
                dlsize = 0
                total_length = int(total_length)
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:  # filter out keep-alive new chunks
                        f.write(chunk)
                        f.flush()
                        dlsize += len(chunk)

                        Reporter.report(dlsize, total_length)
            print("")


def run():
    args = get_args()

    # Setup logger
    root = logging.getLogger()
    handler = logging.StreamHandler()
    bf = LogFormatter('%(levelname)s:%(module)s:%(message)s')
    handler.setFormatter(bf)
    root.addHandler(handler)
    if args.verbose:
        root.setLevel(logging.DEBUG)
    else:
        root.setLevel(logging.CRITICAL)

    # Work on chosen site
    downloader = Downloader(
        workers=args.workers,
        print_as_info=args.print_info,
        player=args.player
    )
    site = wrappers.get_instance(args.site)
    if not site:
        print("ERROR: Not an available site")
        print("")
        print("List of valid sites: ")
        for site in wrappers.get_instances():
            print("  {}".format(site.name))
        print("")

        return 1

    if args.search:
        query = args.search
        media_list = site.search(query)
        for media in media_list:
            fstr = "{} {!r} ({})".format(media['tags'], media['title'], media['url'])
            print(fstr)

    if args.url and args.code:
        url = args.url
        code = args.code
        stream_urls = site.get_urls(url, code=code)

        if args.extract or args.play or args.download:
            downloader.extract(stream_urls)
            if args.download:
                downloader.download()
            if args.play:
                downloader.play()
        else:
            for stream_url in stream_urls:
                print(stream_url)
