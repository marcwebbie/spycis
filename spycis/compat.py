import sys

if sys.version_info < (3,):
    # fallback to python2
    input = raw_input
    str = unicode

try:
    import StringIO
except ImportError:
    from io import StringIO
