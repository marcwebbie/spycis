from functools import partial
from mimetypes import guess_extension, guess_type
import os
import re
import requests
from requests.exceptions import RequestException
import sys

if sys.version_info >= (3,):
    from queue import Queue
    from urllib.parse import urlparse, urlunparse, unquote
    from urllib.request import urljoin
    from io import StringIO
else:
    # fallback to python2
    from Queue import Queue
    from urllib import unquote
    from urlparse import urlparse, urlunparse, urljoin
    from StringIO import StringIO
from .compat import *
from .extractors import get_instances


session = requests.Session()
headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:26.0) Gecko/20100101 Firefox/26.0"}
session.headers.update(headers)
http_adapter = requests.adapters.HTTPAdapter(pool_connections=100, pool_maxsize=100)
session.mount('http://', http_adapter)
# patch session to use timeout
session.get = partial(session.get, timeout=3)
session.post = partial(session.post, timeout=3)


def baseconv(number, base=10):
    alphabet = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'.lower()
    result = ''
    while number:
        number, i = divmod(number, base)
        result = alphabet[i] + result

    return result or alphabet[0]


def unpacker(p, a, c, k, e=None, d=None):
    for c in reversed(range(c)):
        if(k[c]):
            p = re.sub(r'\b' + baseconv(c, base=a) + r'\b', k[c], p)
    return p


class Color(object):
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    END = "\033[0m"


def set_color(s, color):
    return "{}{}{}".format(color, s, Color.END)


def get_absolute_path(path):
    parsed = urlparse(path)
    filepath = os.path.abspath(os.path.join(parsed.netloc, parsed.path))
    return filepath


def is_raw_url(url):
    parsed_url = urlparse(url)
    url_scheme = parsed_url.scheme
    url_path = parsed_url.path
    try:
        url_extension = guess_extension(guess_type(url_path)[0])
    except AttributeError:
        return None

    valid_extensions = ('.flv', '.mp4', '.avi', '.mkv', '.m4v', '.webm', '.mp3', '.aac', '.ogg')
    valid_schemes = ('http', 'https', 'ftp', 'udp')

    if url_scheme in valid_schemes and url_extension in valid_extensions:
        return True
    else:
        return False


def is_stream_url(url):
    return any(extractor.is_valid_url(url) for extractor in get_instances())


def is_local_file(path):
    parsed = urlparse(path)
    filepath = os.path.abspath(os.path.join(parsed.netloc, parsed.path))

    return os.path.isfile(filepath)


def print_error(message, flush=True):
    sys.stderr.write("{}\n".format(message))
    if flush:
        sys.stderr.flush()
