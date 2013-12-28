
class BaseWrapper(object):

    @property
    def name(self):
        class_name = self.__class__.__name__.lower().replace('wrapper', '')
        return class_name
