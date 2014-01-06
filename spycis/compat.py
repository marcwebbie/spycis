import sys

if sys.version_info >= (3,):
    from queue import Queue
    from urllib.parse import urlparse, urlunparse, unquote
    from io import StringIO
    input = input
else:
    # fallback to python2
    from Queue import Queue
    from urllib import unquote
    from urlparse import urlparse, urlunparse
    from StringIO import StringIO
    input = raw_input
