import abc


class FieldFilter(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, field_name, filter_args):
        self.field_name = field_name
        self.filter_args = filter_args

    # TODO: Put it back when we need it
    # @abc.abstractmethod
    def on_django_query(self, query):
        pass

    # TODO: Put it back when we need it
    # @abc.abstractmethod
    def on_sqlalchemy_query(self, query):
        pass

    @abc.abstractmethod
    def on_dicts(self, dicts):
        pass
