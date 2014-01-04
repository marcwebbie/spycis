import os
import requests

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1674.0 Safari/537.36"
}
session = requests.Session()
session.headers.update(headers)
http_adapter = requests.adapters.HTTPAdapter(pool_connections=100, pool_maxsize=100)
session.mount('http://', http_adapter)


def baseconv(number, base=10):
    alphabet = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'.lower()
    result = ''
    while number:
        number, i = divmod(number, base)
        result = alphabet[i] + result

    return result or alphabet[0]


class Color(object):
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    END = "\033[0m"


def set_color(s, color):
    return "{}{}{}".format(color, s, Color.END)
