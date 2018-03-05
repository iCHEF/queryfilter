from __future__ import absolute_import
from six import add_metaclass
import abc

from .base import FieldFilter
from .queryfilter import QueryFilter


@add_metaclass(abc.ABCMeta)
class TextMatchMixin(object):
    @abc.abstractmethod
    def _is_value_matched(self, value): pass

    def get_query_value(self):
        return self.filter_args["value"]

    def on_dicts(self, dicts):
        return [
            d for d in dicts
            if self._is_value_matched(d.get(self.field_name))
        ]


@QueryFilter.register_type_condition('string', 'equals')
class TextFullyMatchedFilter(TextMatchMixin, FieldFilter):
    def _is_value_matched(self, value):
        return bool(value == self.get_query_value())


@QueryFilter.register_type_condition('string', 'contains')
class TextPartialMatchedFilter(TextMatchMixin, FieldFilter):
    def _is_value_matched(self, value):
        return bool(self.get_query_value() in value)


@QueryFilter.register_type_condition('string', 'starts_with')
class TextStartsWithMatchedFilter(TextMatchMixin, FieldFilter):
    def _is_value_matched(self, value):
        return bool(value.startswith(self.get_query_value()))


@QueryFilter.register_type_condition('string', 'ends_with')
class TextEndsWithMatchedFilter(TextMatchMixin, FieldFilter):
    def _is_value_matched(self, value):
        return bool(value.endswith(self.get_query_value()))
