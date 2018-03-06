from __future__ import absolute_import
from six import add_metaclass
import abc

from .base import FieldFilter, DictFilterMixin
from .queryfilter import QueryFilter


@add_metaclass(abc.ABCMeta)
class TextMatchMixin(DictFilterMixin):
    @abc.abstractmethod
    def _is_value_matched(self, value): pass

    def get_query_value(self):
        return self.filter_args["value"]

    def on_dicts(self, dicts):
        kept_dicts = []
        for d in dicts:
            field_value = self.get(d, self.field_name)
            if field_value is None:
                self.false_with_drop_none_else_raise(self.field_name)
                continue  # skip on field value None
            if self._is_value_matched(field_value):
                kept_dicts.append(d)
        return kept_dicts


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
