#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
import re
import random
import socket
import subprocess
import sys
from threading import Thread
import time

from spycis import extractors
from spycis.utils import Queue, urlparse


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

    def __init__(self, workers=0, raw_url_info=False):
        self.workers = workers
        self.raw_url_info = raw_url_info
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
                    if self.raw_url_info:
                        sys.stdout.write("{0}\n".format(info))
                    sys.stdout.write("{0}\n".format(info['url']))
                    sys.stdout.flush()
                    self.info_list.append(info)
            else:
                logging.warning("Couldn't get extractor for url: {0}".format(url))

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
        if self.raw_url_info:
            logging.debug("Extracting raw urls with info")
        if self.workers > 0:
            return self.extract_async(stream_urls)

        for url in stream_urls:
            extractor = next((e for e in self.extractor_list if e.is_valid_url(url)), None)
            if extractor:
                info = extractor.extract(url)
                if info:
                    print(info if self.raw_url_info else info['url'])
                    self.info_list.append(info)

    def stream(self, pattern, stream_port, subtitles):
        pattern = re.compile(pattern)
        try:
            matched_infos = [
                i for i in self.info_list
                if pattern.search(i['webpage_url']) or
                pattern.search(i['url']) or
                pattern.search(i['title'])
            ]
            info = random.choice(matched_infos)
        except IndexError:
            logging.warning("streaming: No raw url matched pattern: '{}'".format(pattern.pattern))
            return None
        else:
            video_path = info['url']
            subs_path = subtitles
            if not subs_path:
                prompt = "Glissez les sous-titres pour {!r} ici : ".format(
                    info['title'])
                subs_path = input(prompt).strip().strip('"\'')
                subs_path = urlparse(subs_path).path

            command = [
                "cvlc",
                "{}".format(video_path),
                "--sub-file={}".format(subs_path) if subs_path else "--sub-autodetect-file",
                "--file-caching=3000",
                "--sout=#transcode{venc=x264{level=30,"
                "keyint=15,bframes=0,ref=1,nocabac},width=640,vcodec=x264,vb=400,acodec=mpga,ab=96,channels=2,samplerate=44100,scodec=dvbs,soverlay,threads==4}:http{mux=ts,dst=:%s/}" % stream_port
            ]

            addr = socket.gethostbyname(socket.gethostname())
            print(' * Playing file at: {}'.format(info['url']))
            print(' * Streaming from: {}:{}'.format(addr, stream_port))
            return subprocess.call(command)

    def play(self, pattern, player):
        pattern = re.compile(pattern)
        try:
            matched_infos = [
                i for i in self.info_list
                if pattern.search(i['webpage_url']) or
                pattern.search(i['url']) or
                pattern.search(i['title'])
            ]
            info = random.choice(matched_infos)
        except IndexError:
            logging.warning("play: No raw url matched pattern: '{}'".format(pattern.pattern))
            return None
        else:
            logging.debug('Chosen info to play: {}'.format(info))

            command = [
                player,
                info['url'],
            ]

            if player in ("vlc", "cvlc"):
                command.extend([
                    "--sub-autodetect-file",
                    "--file-caching=3000",
                ])

            print(' * Playing file at: {}'.format(info['url']))
            return subprocess.call(command)

    def download(self, pattern):
        pattern = re.compile(pattern)
        try:
            matched_infos = [
                i for i in self.info_list if pattern.search(i['webpage_url']) or
                pattern.search(i['url']) or
                pattern.search(i['title'])
            ]
            info = random.choice(matched_infos)
        except IndexError:
            logging.warning("download: No raw url matched pattern: '{}'".format(pattern.pattern))
            return None
        else:
            agent = "Mozilla/5.0 (X11; Linux x86_64; rv:26.0) Gecko/20100101 Firefox/26.0"
            url = info["url"]
            command = ['wget', '-U', agent, url]

            local_filename = info['title']
            if local_filename:
                if info['ext'] not in local_filename:
                    local_filename = "{}{}".format(
                        info['title'], info['ext'])
                command.extend(['-O', local_filename])

            return subprocess.call(command)
