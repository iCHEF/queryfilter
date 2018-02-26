from __future__ import absolute_import
from six import add_metaclass
import abc

from .base import FieldFilter


@add_metaclass(abc.ABCMeta)
class TextMatchMixin(object):
    @abc.abstractmethod
    def _is_value_matched(self, value): pass

    def on_dicts(self, dicts):
        return [
            d for d in dicts
            if self._is_value_matched(d.get(self.field_name))
        ]


class TextFullyMatchedFilter(TextMatchMixin, FieldFilter):
    filter_type = "string"
    filter_condition = "equals"

    def _is_value_matched(self, value):
        return bool(value == self.filter_args["value"])


class TextPartialMatchedFilter(TextMatchMixin, FieldFilter):
    filter_type = "string"
    filter_condition = "contains"

    def _is_value_matched(self, value):
        return bool(self.filter_args["value"] in value)


class TextStartWithMatchedFilter(TextMatchMixin, FieldFilter):
    filter_type = "string"
    filter_condition = "contains"

    def _is_value_matched(self, value):
        return bool(value.startswith(self.filter_args["value"]))


class TextEndWithMatchedFilter(TextMatchMixin, FieldFilter):
    filter_type = "string"
    filter_condition = "contains"

    def _is_value_matched(self, value):
        return bool(value.endswith(self.filter_args["value"]))
