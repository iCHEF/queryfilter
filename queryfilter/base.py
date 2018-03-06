import abc

from .exceptions import (
    FilterOnNoneValue,
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
        self.options = {
            "drop_none": True
        }
        passed_in_options = options if options else {}
        self.options.update(passed_in_options)

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
        raise FilterOnNoneValue(field_name)


class DictFilterMixin(object):
    def __init__(self, *args, **kwargs):
        super(DictFilterMixin, self).__init__(*args, **kwargs)
        options_kwargs = kwargs.get("options", {})
        option_kw_value = options_kwargs.get("none_for_missing_field", True)
        self.options["none_for_missing_field"] = option_kw_value

    def get(self, dictobj, field_name):
        if (field_name not in dictobj) and (
                not self.options["none_for_missing_field"]):
            raise FieldNotFound(field_name)
        return dictobj.get(field_name)
