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

    def _do_django_query(self, queryset):

        if not self.choices:
            return queryset.none()

        query = {
            self.field_name + "__in": self.choices
        }

        return queryset.filter(**query)
