import inspect
import os
import glob

from .common import BaseWrapper, Media, Episode, Stream

__all__ = [os.path.basename(f)[:-3]
           for f in glob.glob(os.path.dirname(__file__) + "/*.py")]


def _import_all_wrapper_files():
    __import__(__name__, globals(), locals(), __all__, 0)


def get_all():
    """Get all subclasses of BaseWrapper from module and return and generator
    """

    _import_all_wrapper_files()

    for module in (value for key, value in globals().items() if key in __all__):
        for klass_name, klass in inspect.getmembers(module, inspect.isclass):
            if klass is not BaseWrapper and issubclass(klass, BaseWrapper):
                yield klass


def get_instances():
    """Get instances of all found detected wrapper classes"""
    return (wclass() for wclass in get_all())


def get_instance(name):
    for wrapper in get_instances():
        if wrapper.name == name:
            return wrapper
