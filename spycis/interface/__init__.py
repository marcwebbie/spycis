import argparse
import logging
import subprocess
from threading import Thread
try:
    from queue import Queue
except ImportError:
    # fallback to python2
    from Queue import Queue


from spycis import extractors, wrappers


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
    aparser.add_argument("--print-info", action="store_true", help="print info instead of urls")
    aparser.add_argument("--player", default="cvlc", help="specify the player to use for the --play option, ex: --player vlc")
    args = aparser.parse_args()

    return args


class Downloader(object):

    def __init__(self, workers=None, print_as_info=False, player="cvlc"):
        self.timeout = 5
        self.workers = workers
        self.download_queue = Queue()
        self.print_as_info = print_as_info
        self.extractor_list = list(extractors.get_instances())
        self.info_list = []
        self.player = player

    def _extract_worker(self):
        while True:
            url = self.download_queue.get()
            logging.debug("init downloading from url: {}".format(url))

            extractor = next((e for e in self.extractor_list if e.is_valid_url(url)), None)
            if extractor:
                info = extractor.extract(url)
                if info:
                    print(info if self.print_as_info else info['url'])
                    self.info_list.append(info)
            else:
                logging.debug("Couldn't get extractor for url: {0}".format(url))

            self.download_queue.task_done()

    def spawn_workers(self):
        for i in range(self.workers):
            worker = Thread(target=self._extract_worker)
            worker.daemon = True
            worker.start()
            logging.debug("started worker: {}".format(i + 1))

    def extract_async(self, stream_urls):
        self.spawn_workers()
        for url in stream_urls:
            self.download_queue.put(url)
            logging.debug("Added url to extract queue: {}".format(url))
        return self.download_queue.join()

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
        available_wrappers = wrappers.get_instances()
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

        if args.extract or args.play:
            downloader.extract(stream_urls)
            if args.play:
                downloader.play()
        else:
            for stream_url in stream_urls:
                print(stream_url)
