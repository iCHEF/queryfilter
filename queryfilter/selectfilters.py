from __future__ import absolute_import, unicode_literals

from .base import FieldFilter, DjangoQueryFilterMixin
from .queryfilter import QueryFilter


@QueryFilter.register_type_condition('select')
class SelectFilter(DjangoQueryFilterMixin, FieldFilter):

    @property
    def choices(self):
        return self.filter_args.get("values", [])

    def on_dicts(self, dicts):

        return [
            d for d in dicts
            if d.get(self.field_name) in self.choices
        ]

    @property
    def query_params(self):
        return {
            self.field_name + "__in": self.choices
        } if self.choices else None

    def _do_django_query(self, queryset):
        query_params = self.query_params

        if query_params is None:
            return queryset.none()

        return queryset.filter(**query_params)
