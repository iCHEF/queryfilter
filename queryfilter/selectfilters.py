from __future__ import absolute_import

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

    def do_filter(self, queryset):

        if not self.choices:
            return queryset.none()

        query = {u"{field_name}__in".format(field_name=self.field_name): self.choices}

        return queryset.filter(**query)

