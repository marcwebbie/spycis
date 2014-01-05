#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import argparse
from mimetypes import guess_extension, guess_type
import logging
import random
import os
import socket
import subprocess
import sys
from tempfile import NamedTemporaryFile
from threading import Thread
import time
try:
    from queue import Queue
    from urllib.parse import urlparse, urlunparse
except ImportError:
    # fallback to python2
    from Queue import Queue
    from urlparse import urlparse, urlunparse
    input = raw_input

from spycis import extractors, wrappers
from spycis.utils import session, Color, set_color, get_absolute_path


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


def get_version():
    version_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), '__version__.py')
    version = open(version_file).read().strip()
    return version


def get_args():
    aparser = argparse.ArgumentParser()

    aparser.add_argument("-r", "--raw-urls", help="Retourne les raw urls pour le code ou specifié. ex: `-r s02e31` ou `--raw-urls  s02e31`")
    aparser.add_argument("-s", "--stream-urls", help="Retourne les stream urls pour le code specifié. ex: `-s s02e31` ou `--stream-urls  s02e31`")
    aparser.add_argument("-p", "--position", type=int, default=-1,
                         help="Options utilisé avec `-r` ou `-s` pour specifié la positon¹. ex: `-p 2 -r s02e31`")

    aparser.add_argument("--play", help="Executer le premier fichier au format specifié dans les `raw urls` extraites. ex: `--play mp4`")
    aparser.add_argument("--player", default="vlc", help="Choisir le player pour l'option play ex: `--player amarok`")
    aparser.add_argument("--download", help="Télécharge le premier fichier en format dans les `raw urls` extraites. ex: `--download mp4`")
    aparser.add_argument("--stream", help="Ouvre streaming sur la porte specifié. ex: `--stream 8080`")
    aparser.add_argument("--subtitles", help="Ouvre streaming pour les soustitres ex: `--subtitles mes_sous_titres.srt`")

    aparser.add_argument("--udp", action="store_true", help="active stream par udp protocol")
    aparser.add_argument("-v", "--verbose", action="store_true", help="active le mode verbose pour debugging")
    aparser.add_argument("--site", default="tubeplus", help="Changer le site de recherche. ex: `--site sitename`")
    aparser.add_argument("-w", "--workers", action="store", type=int, default=8,
                         help="Nombre des threads pour l'extraction des urls ex: `--workers 20`")
    aparser.add_argument("--version", action='version', version=get_version(), help="imprime version et quitte")

    aparser.add_argument("query", help="L'argument principale pour les recherches")

    args = aparser.parse_args()
    return args


class Reporter(object):

    last_time = time.time()
    last_length = 0
    last_dlrate = "0 K"

    @staticmethod
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

    def __init__(self, workers=None, print_as_info=False):
        self.workers = workers
        self.print_as_info = print_as_info
        self.extraction_queue = Queue()
        self.extractor_list = list(extractors.get_instances())

        self.info_list = []

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

    def stream(self, stream_port, subtitles, udp=False):
        info = random.choice(self.info_list)

        if info:
            video_path = info['url']
            subtitle_path = subtitles
            if not subtitle_path:
                subtitle_path = input("Glissez les sous-titres pour {!r} ici : ".format(info['title'])).strip().strip('"\'')
                subtitle_path = urlparse(subtitle_path).path
                subtitle_path = subtitle_path if subtitle_path else NamedTemporaryFile('w', delete=False).name

            cmd = [
                "cvlc",
                "{}".format(video_path),
                "--sub-file={}".format(subtitle_path),
                "--file-caching=3000",
                # "--sout=#transcode{vcodec=h264,venc=x264{profile=baseline,level=30,keyint=30,ref=3},acodec=mp3,ab=96,scodec=dvbs,soverlay,threads=4}:http{mux=ts,dst=:%s/}" % stream_port
                "--sout=#transcode{venc=x264{level=30,keyint=15,bframes=0,ref=1,nocabac},width=640,vcodec=x264,vb=400,acodec=mpga,ab=96,channels=2,samplerate=44100,scodec=dvbs,soverlay,threads==4}:http{mux=ts,dst=:%s/}" % stream_port
            ]

            addr = socket.gethostbyname(socket.gethostname())
            sys.stderr.write(' * Streaming from: {}:{}\n'.format(addr, stream_port))
            sys.stderr.write('\n'.format(addr))
            sys.stderr.flush()

            return subprocess.call(cmd)
        else:
            sys.stderr.write("Couldn't find a match url for the stream\n")
            sys.stderr.flush()
            return None

    def play(self, extension, player):
        info = next((i for i in self.info_list), None)

        if info:
            command = [
                player,
                info['url'],
            ]

            if player in ("vlc", "cvlc"):
                command.extend([
                    "--file-caching=1000",
                ])
            subprocess.call(command)
        else:
            logging.warning("Couldn't find video file with extension: {}", extension)

    def download(self):
        for elem in self.info_list:
            info = elem
            if info['ext'] == 'mp4':
                break

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


def is_raw_url(url):
    logging.debug("Testing if is raw url: {}".format(url))
    logging.debug("Parsed url: {}".format(urlparse(url)))

    if os.path.isfile(url):
        url = urlunparse(urlparse(os.path.abspath(url))._replace(scheme='file'))

    parsed_url = urlparse(url)
    url_scheme = parsed_url.scheme
    url_path = parsed_url.path
    try:
        url_extension = guess_extension(guess_type(parsed_url.path)[0])
    except AttributeError:
        logging.warning("Url n'a pas d'extension")
        return None

    valid_extensions = ('.flv', '.mp4', '.avi', '.mkv', '.m4v', '.webm', '.mp3', '.aac', '.ogg')
    valid_schemes = ('http', 'https', 'ftp', 'udp', 'file')

    if url_scheme in valid_schemes and url_extension in valid_extensions:
        return parsed_url
    else:
        return False


def is_local_file(path):
    parsed = urlparse(path)
    filepath = os.path.abspath(os.path.join(parsed.netloc, parsed.path))

    return os.path.isfile(filepath)


def run():
    args = get_args()

    # print("==============================")
    # print(args)
    # print("==============================")

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

    if site.is_valid_url(args.query):
        url = args.query
        code = args.raw_urls if args.raw_urls else args.stream_urls
        stream_urls = site.get_urls(url, code=code)
        if args.raw_urls:
            downloader.extract(stream_urls)
        else:
            for stream_url in stream_urls:
                print(stream_url)

    elif any(ext.is_valid_url(args.query) for ext in extractors.get_instances()):
        url = args.query
        downloader.extract([url])

    elif is_raw_url(url=args.query):
        url = is_raw_url(url=args.query)
        title = os.path.basename(url)
        extension = guess_extension(guess_type(parsed_url.path)[0])

        info = {
            "id": "unknown",
            "title":  title,
            "url": url,
            "ext": extension,
        }
        downloader.info_list.append(info)

    elif is_local_file(path=args.query):
        filepath = get_absolute_path(args.query)
        title = os.path.basename(url)
        extension = guess_extension(guess_type(parsed_url.path)[0])

        info = {
            "id": "unknown",
            "title":  title,
            "url": url,
            "ext": extension,
        }
        downloader.info_list.append(info)

    elif args.stream_urls:
        query = args.query
        search_result = site.search(query)

        position = args.position if args.position >= 0 else 0
        try:
            url = search_result[position]['url']
        except IndexError:
            raise IndexError("Position non valide")

        code = args.stream_urls
        stream_urls = site.get_urls(url, code=code)

        for stream_url in stream_urls:
            print(stream_url)

    elif args.raw_urls:
        query = args.query
        search_result = site.search(query)

        position = args.position if args.position >= 0 else 0
        try:
            url = search_result[position]['url']
        except IndexError:
            raise IndexError("Position non valide")

        code = args.raw_urls
        stream_urls = site.get_urls(url, code=code)
        downloader.extract(stream_urls)

    elif args.position >= 0:
        """Obtenir les raw urls pour la position de recherche 30. 
        Attention ça marche que pour les film, pour les series au moins 
        un code episode doit être informé au format:-p 30 -r s01e01"""
        query = args.query
        search_result = site.search(query)
        position = args.position
        try:
            url = search_result[position]['url']
        except IndexError:
            raise IndexError("Position non valide")

        stream_urls = site.get_urls(url, code=None)
        downloader.extract(stream_urls)
    else:
        query = args.query

        if is_raw_url(url) or urlparse(query).scheme:
            logging.warning("Can't do search on urls")
        else:
            search_result = site.search(query)
            for position, result in enumerate(search_result):
                fstr = "{0:<15} {1:<13} {2:50} ({3})".format(
                    "[{}]".format(set_color(position, Color.YELLOW)),
                    result['tags'],
                    set_color(repr(result['title']), Color.GREEN),
                    result['url']
                )
                print(fstr)

    # Bonus options
    if args.play and downloader.info_list:
        extension = args.play
        player = args.player
        downloader.play(extension=extension, player=player)
    elif args.stream and downloader.info_list:
        stream_port = args.stream
        subtitles = args.subtitles
        downloader.stream(stream_port=stream_port, subtitles=subtitles, udp=args.udp)
