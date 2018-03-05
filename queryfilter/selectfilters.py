from __future__ import absolute_import

from .base import FieldFilter
from .queryfilter import QueryFilter


@QueryFilter.register_type_condition('select')
class SelectFilter(FieldFilter):
    def get_query_selections(self):
        return self.filter_args.get("values", [])

    def on_dicts(self, dicts):
        selections = self.get_query_selections()

        return [
            d for d in dicts
            if d.get(self.field_name) in selections
        ]
