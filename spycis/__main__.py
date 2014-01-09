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


__version__ = "0.0.1-dev4"


def get_logger():
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
            fmessage = "{0}{1:<.200}{2}".format(
                LogFormatter.color[level],
                final_msg,
                LogFormatter.color['ENDC'],
            )
            return fmessage

    root = logging.getLogger()
    handler = logging.StreamHandler()
    bf = LogFormatter('%(levelname)s:%(module)s:%(message)s')
    handler.setFormatter(bf)
    root.addHandler(handler)

    return root


def get_version():
    return "Spycis v{}".format(__version__)


def get_args():
    aparser = argparse.ArgumentParser()

    aparser.add_argument("-r", "--raw-urls",
                         help="Retourne les raw urls pour le code. "
                         "ex: `-r s02e31` ou `--raw-urls  s02e31`")
    aparser.add_argument("-s", "--stream-urls",
                         help="Retourne les stream urls pour le code "
                         ". ex: `-s s02e31` ou `--stream-urls  s02e31`")
    aparser.add_argument("-p", "--position", type=int, default=0,
                         help="Options utilisé avec `-r` ou `-s` pour "
                         "specifié la positon¹. ex: `-p 2 -r s02e31`")

    aparser.add_argument("--play",
                         help="Executer le premier fichier que "
                         "match le pattern. ex: `--play mp4`")
    aparser.add_argument("--player", default="vlc",
                         help="Choisir le player pour l'option play "
                         "ex: `--player amarok`")
    aparser.add_argument("--download",
                         help="Télécharge le premier fichier "
                         "que match le pattern. ex: `--download mp4`")
    aparser.add_argument("--stream",
                         help="Ouvre streaming sur la porte specifié. "
                         "ex: `--stream 8080`")
    aparser.add_argument("--stream-port", default=8080, type=int,
                         help="Choisir le player pour l'option play "
                         "ex: `--player amarok`")
    aparser.add_argument("--subtitles",
                         help="Ouvre streaming pour les soustitres "
                         "ex: `--subtitles mes_sous_titres.srt`")

    aparser.add_argument("-v", "--verbose", action="count",
                         help="active le mode verbose pour debugging")
    aparser.add_argument("--site", default="tubeplus",
                         help="Changer le site de recherche. "
                         "ex: `--site sitename`")
    aparser.add_argument("--site-list", action="store_true",
                         help="lister les sites de recherche disponibles")
    aparser.add_argument("--workers", action="store", type=int, default=8,
                         help="Nombre des threads pour l'execution "
                         "ex: `--workers 20`")
    aparser.add_argument("--version", action='version',
                         version=get_version(), help="imprime version")

    aparser.add_argument("query",
                         help="L'argument principale pour les recherches")

    args = aparser.parse_args()
    return args


def print_available_sites():
    print("")
    print("List of available sites: ")
    for site in wrappers.get_instances():
        print("  {}".format(site.name))
    print("")


def clean_search_by_code(func):
    from functools import wraps

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            print('{}'.format(e.message))
            sys.exit(1)
    return wrapper


@clean_search_by_code
def run(args=get_args()):
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
        print("ERROR: Not an available site")
        print_available_sites()
        sys.exit(1)
    elif args.site_list:
        print_available_sites()
        sys.exit(0)

    if site.is_valid_url(url=args.query):
        logging.debug("Found a valid url for site: '{}'".format(args.query))

        url = args.query
        code = args.raw_urls if args.raw_urls else args.stream_urls
        streams = site.get_streams(url, code=code)
        if args.raw_urls:
            downloader.extract(streams)
        else:
            for stream in streams:
                print(stream.url)

    elif is_stream_url(url=args.query):
        logging.debug("Found a valid url for site: '{}'".format(args.query))
        url = args.query
        downloader.extract([url])

    elif is_raw_url(url=args.query):
        url = args.query
        parsed_url = urlparse(url)
        title = os.path.basename(parsed_url.path)
        extension = guess_extension(guess_type(parsed_url.path)[0])

        info = {
            "id": "unknown",
            "title": title,
            "url": url,
            "ext": extension,
        }
        downloader.info_list.append(info)
        logging.debug('added raw url: {}'.format(info['url']))

    elif is_local_file(path=args.query):
        """Ajoute le fichier local a la liste de infos du Downloader"""
        filepath = get_absolute_path(args.query)
        title = os.path.basename(filepath)
        extension = guess_extension(guess_type(title)[0])

        info = {
            "id": "unknown",
            "title": title,
            "url": filepath,
            "ext": extension,
        }
        downloader.info_list.append(info)
        logging.debug('added raw url: {}'.format(info['url']))

    else:
        medias = site.search(args.query)
        try:
            chosen_media_url = medias[args.position].url
        except IndexError:
            logging.error("Not a valid position")
            return None

        code = (args.stream_urls if args.stream_urls else
                args.raw_urls if args.raw_urls else
                None)

        streams = site.get_streams(chosen_media_url, code=code)

        if args.stream_urls:
            """Obtenir les stream urls pour la position 0 ou autre si position specifié"""
            for stream in streams:
                print(stream.url)

        elif args.raw_urls:
            """Obtenir les raw urls pour la position 0 ou autre si position specifié"""
            downloader.extract(s.url for s in streams)

        elif args.position:
            """Obtenir les raw urls pour la position de recherche specifié.

            Attention ça marche que pour les film, pour les series au moins
            un code episode doit être informé au format:-p 30 -r s01e01"""
            downloader.extract(s.url for s in streams)

        else:
            for position, media in enumerate(medias):
                position_line = "{0:<15} {1:<13} {2:<55} [{3}] ({4})".format(
                    "[{}]".format(set_color(position, Color.YELLOW)),
                    [media.category],
                    set_color(repr("{:.42}".format(media.title)), Color.GREEN),
                    set_color(media.year, Color.YELLOW) if media.year else None,
                    media.url,
                )
                print(position_line)

    # Bonus options
    if args.play:
        if downloader.info_list:
            pattern = args.play
            player = args.player
            downloader.play(pattern=pattern, player=player)
        else:
            logging.warning(
                'No raw urls were found to proceed with playing'
                ' try running with -r ou --raw-urls argument')

    elif args.stream:
        if downloader.info_list:
            pattern = args.stream
            stream_port = args.stream_port
            subtitles = args.subtitles
            downloader.stream(pattern=pattern,
                              stream_port=stream_port,
                              subtitles=subtitles)
        else:
            logging.warning(
                'No raw urls were found to proceed with streaming'
                ' try running with -r ou --raw-urls argument')

    elif args.download:
        if downloader.info_list:
            pattern = args.download
            downloader.download(pattern=pattern,)
        else:
            logging.warning(
                'No raw urls were found to proceed with download'
                ' try running with -r ou --raw-urls argument')

if __name__ == '__main__':
    try:
        run()
    except KeyboardInterrupt:
        sys.stderr.flush()
        print("")
