import abc

from .exceptions import (
    FilterOnNoneValueError,
    FieldNotFound
)


class FieldFilter(object):
    __metaclass__ = abc.ABCMeta

    def __init__(
            self,
            field_name,
            filter_args,
            options=None
    ):
        self.field_name = field_name
        self.filter_args = filter_args
        default_filter_options = {
            "drop_none": True
        }
        self.options = options or default_filter_options

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

    def false_with_drop_none_else_raise(self, field_name):
        if self.options["drop_none"]:
            return False
        raise FilterOnNoneValueError(field_name)


class BaseDictFilter(object):
    def __init__(self, *args, **kwargs):
        super(BaseDictFilter, self).__init__(*args, **kwargs)
        options_kwarg = kwargs["options"]
        none_for_missing_field = options_kwarg.get("none_for_missing_field", True)
        self.options["none_for_missing_field"] = none_for_missing_field

    def get(self, dictobj, field_name):
        if (field_name not in dictobj) and (
                not self.options["none_for_missing_field"]):
            raise FieldNotFound(field_name)
        return dictobj.get(field_name)
