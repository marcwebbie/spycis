#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Execute with
# $ python spycis/__main__.py (2.6+)
# $ python -m spycis          (2.7+)

from __future__ import (
    absolute_import, division, generators,
    unicode_literals, print_function,
    nested_scopes, with_statement
)

import sys
import argparse
from mimetypes import guess_extension, guess_type
import logging
import os

if __package__ is None and not hasattr(sys, "frozen"):
    # direct call of __main__.py
    path = os.path.realpath(os.path.abspath(__file__))
    sys.path.append(os.path.dirname(os.path.dirname(path)))

from spycis import wrappers
from spycis.compat import urlparse
from spycis.downloader import Downloader
from spycis.utils import (
    Color,
    set_color,
    get_absolute_path,
    is_local_file,
    is_stream_url,
    is_raw_url
)


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


def get_logger():
    root = logging.getLogger()
    handler = logging.StreamHandler()
    bf = LogFormatter('%(levelname)s:%(module)s:%(message)s')
    handler.setFormatter(bf)
    root.addHandler(handler)

    return root


def get_version():
    return "not set"


def get_args():
    aparser = argparse.ArgumentParser()

    aparser.add_argument("-r", "--raw-urls", help="Retourne les raw urls pour le code ou specifié. ex: `-r s02e31` ou `--raw-urls  s02e31`")
    aparser.add_argument("-s", "--stream-urls", help="Retourne les stream urls pour le code specifié. ex: `-s s02e31` ou `--stream-urls  s02e31`")
    aparser.add_argument("-p", "--position", type=int, default=0,
                         help="Options utilisé avec `-r` ou `-s` pour specifié la positon¹. ex: `-p 2 -r s02e31`")

    aparser.add_argument("--play", help="Executer le premier fichier au format specifié dans les `raw urls` extraites. ex: `--play mp4`")
    aparser.add_argument("--player", default="vlc", help="Choisir le player pour l'option play ex: `--player amarok`")
    aparser.add_argument("--download", help="Télécharge le premier fichier en format dans les `raw urls` extraites. ex: `--download mp4`")
    aparser.add_argument("--stream", help="Ouvre streaming sur la porte specifié. ex: `--stream 8080`")
    aparser.add_argument("--subtitles", help="Ouvre streaming pour les soustitres ex: `--subtitles mes_sous_titres.srt`")

    aparser.add_argument("-v", "--verbose", action="count", help="active le mode verbose pour debugging")
    aparser.add_argument("--site", default="tubeplus", help="Changer le site de recherche. ex: `--site sitename`")
    aparser.add_argument("--workers", action="store", type=int, default=4,
                         help="Nombre des threads pour l'extraction des urls ex: `--workers 20`")
    aparser.add_argument("--version", action='version', version=get_version(), help="imprime version et quitte")

    aparser.add_argument("query", help="L'argument principale pour les recherches")

    args = aparser.parse_args()
    return args


def print_available_sites():
    print("ERROR: Not an available site")
    print("")
    print("List of available sites: ")
    for site in wrappers.get_instances():
        print("  {}".format(site.name))
    print("")


def run(args):
    # print(args)

    logger = get_logger()
    if args.verbose:
        logger.setLevel(logging.DEBUG)
        raw_url_info = True if args.verbose > 1 else False
    else:
        logger.setLevel(logging.CRITICAL)
        raw_url_info = False

    downloader = Downloader(workers=args.workers, raw_url_info=raw_url_info)
    site = wrappers.get_instance(args.site)
    if not site:
        print_available_sites()
        return 1

    if site.is_valid_url(url=args.query):
        logging.debug("Found a valid url for site: '{}'".format(args.query))

        url = args.query
        code = args.raw_urls if args.raw_urls else args.stream_urls
        stream_urls = site.get_urls(url, code=code)
        if args.raw_urls:
            downloader.extract(stream_urls)
        else:
            for stream_url in stream_urls:
                print(stream_url)

    elif is_stream_url(url=args.query):
        logging.debug("Found a valid url for site: '{}'".format(args.query))
        url = args.query
        downloader.extract([url])

    elif is_raw_url(url=args.query):
        parsed_url = urlparse(args.query)
        title = os.path.basename(parsed_url.path)
        extension = guess_extension(guess_type(parsed_url.path)[0])

        info = {
            "id": "unknown",
            "title": title,
            "url": url,
            "ext": extension,
        }
        downloader.info_list.append(info)

    elif is_local_file(path=args.query):
        """Ajoute le fichier local a la liste de infos du Downloader"""
        filepath = urlparse(get_absolute_path(args.query)).path
        title = os.path.basename(filepath)
        extension = guess_extension(guess_type(title)[0])

        info = {
            "id": "unknown",
            "title": title,
            "url": url,
            "ext": extension,
        }
        downloader.info_list.append(info)

    elif args.stream_urls:
        """Obtenir les stream urls pour la position 0 ou autre si position specifié"""
        query = args.query
        medias = site.search(query)

        try:
            url = medias[args.position].url
        except IndexError:
            logging.error("Not a valid position")
            return None

        code = args.stream_urls
        stream_urls = site.get_urls(url, code=code)

        for stream_url in stream_urls:
            print(stream_url)

    elif args.raw_urls:
        """Obtenir les raw urls pour la position 0 ou autre si position specifié"""
        query = args.query
        medias = site.search(query)

        try:
            url = medias[args.position].url
        except IndexError:
            logging.error("Not a valid position")
            return None

        code = args.raw_urls
        stream_urls = site.get_urls(url, code=code)
        downloader.extract(stream_urls)

    elif args.position:
        """Obtenir les raw urls pour la position de recherche specifié.

        Attention ça marche que pour les film, pour les series au moins
        un code episode doit être informé au format:-p 30 -r s01e01"""
        query = args.query
        medias = site.search(query)
        position = args.position
        try:
            url = medias[position].url
        except IndexError:
            logging.error("Not a valid position")
            return None

        stream_urls = site.get_urls(url, code=None)
        downloader.extract(stream_urls)
    else:
        query = args.query

        if is_raw_url(query) or is_stream_url(query) or is_local_file(query):
            logging.error("Can't search site for urls or local files")
            return None
        else:
            search_result = site.search(query)

            for position, media in enumerate(search_result):
                position_line = "{0:<15} {1:<13} {2:<55} [{3}] ({4})".format(
                    "[{}]".format(set_color(position, Color.YELLOW)),
                    [media.category],
                    set_color(repr("{:.42}".format(media.title)), Color.GREEN),
                    set_color(media.year, Color.YELLOW) if media.year else None,
                    media.url,
                )
                print(position_line)

    # Bonus options
    if args.play and downloader.info_list:
        extension = args.play
        player = args.player
        downloader.play(extension=extension, player=player)

    elif args.stream and downloader.info_list:
        stream_port = args.stream
        subtitles = args.subtitles
        downloader.stream(stream_port=stream_port, subtitles=subtitles)

    elif args.download and downloader.info_list:
        extension = args.download
        downloader.download(extension=video_format)

if __name__ == '__main__':
    try:
        run(args=get_args())
    except KeyboardInterrupt:
        pass
        print("")
