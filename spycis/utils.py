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


def which(program):
    """
    Mimics behavior of UNIX which command.
    """
    envdir_list = os.environ["PATH"].split(os.pathsep)

    for envdir in envdir_list:
        program_path = os.path.join(envdir, program)
        if os.path.isfile(program_path) and os.access(program_path, os.X_OK):
            return program_path
