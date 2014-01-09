import sys

if sys.version_info < (3,):
    # fallback to python2
    input = raw_input
    str = unicode
