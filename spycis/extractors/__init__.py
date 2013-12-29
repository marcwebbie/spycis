import inspect
import os
import glob

from .common import BaseExtractor

__all__ = [os.path.basename(f)[:-3]
           for f in glob.glob(os.path.dirname(__file__) + "/*.py")]


def _import_all_extractor_files():
    __import__(__name__, globals(), locals(), __all__, 0)


def get_all():
    """Get all subclasses of BaseExtractor from module and return a generator
    """

    _import_all_extractor_files()

    for module in (value for key, value in globals().items() if key in __all__):
        for klass_name, klass in inspect.getmembers(module, inspect.isclass):
            if klass is not BaseExtractor and issubclass(klass, BaseExtractor):
                yield klass


def get_instances():
    """Get instances of all found detected extractor classes"""
    return (extractor_class() for extractor_class in get_all())


def get_extractor(name):
    for extractor in get_instances():
        # print(extractor.name)
        if extractor.name == name:
            return extractor


def get_by_host(host):
    for extractor in get_all():
        if host in extractor.host_list:
            return extractor


def get_by_url(url):
    for extractor in get_all():
        if extractor.is_valid_url(url):
            return extractor
