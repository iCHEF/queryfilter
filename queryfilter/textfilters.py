from __future__ import absolute_import

from django.db.models import Q
from six import add_metaclass
import abc

from .base import FieldFilter, DictFilterMixin, DjangoQueryFilterMixin
from .queryfilter import QueryFilter


@add_metaclass(abc.ABCMeta)
class TextMatchMixin(DjangoQueryFilterMixin, DictFilterMixin):

    @abc.abstractmethod
    def _is_value_matched(self, value):
        pass

    @property
    def query_params(self):
        pass

    @abc.abstractproperty
    def django_lookup_type(self):
        pass

    def get_query_value(self):
        if self.filter_args.get("value"):
            return [
                keyword.strip() for keyword
                in self.filter_args["value"].split(",")
            ]
        return []

    def _do_django_query(self, queryset):
        if self.django_lookup_type:
            lookup_keyword = self.field_name + "__" + self.django_lookup_type
            multi_query = Q()
            for value in self.get_query_value():
                query_params = {
                    lookup_keyword: value
                }
                multi_query = multi_query | Q(**query_params)
            return queryset.filter(multi_query)
        else:
            query_params = {
                self.field_name + "__in": self.get_query_value()
            }
            return queryset.filter(**query_params)

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

    @property
    def django_lookup_type(self):
        return ""

    def _is_value_matched(self, value):
        return bool(value in self.get_query_value())


@QueryFilter.register_type_condition('string', 'contains')
class TextPartialMatchedFilter(TextMatchMixin, FieldFilter):

    @property
    def django_lookup_type(self):
        return "contains"

    def _is_value_matched(self, value):
        return any([
            bool(key_to_match in value)
            for key_to_match in self.get_query_value()
        ])


@QueryFilter.register_type_condition('string', 'starts_with')
class TextStartsWithMatchedFilter(TextMatchMixin, FieldFilter):

    @property
    def django_lookup_type(self):
        return "startswith"

    def _is_value_matched(self, value):
        return any([
            bool(value.startswith(key_to_match))
            for key_to_match in self.get_query_value()
        ])


@QueryFilter.register_type_condition('string', 'ends_with')
class TextEndsWithMatchedFilter(TextMatchMixin, FieldFilter):

    @property
    def django_lookup_type(self):
        return "endswith"

    def _is_value_matched(self, value):
        return any([
            bool(value.endswith(key_to_match))
            for key_to_match in self.get_query_value()
        ])
