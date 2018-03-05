from __future__ import absolute_import

from .base import FieldFilter
from .queryfilter import QueryFilter


@QueryFilter.register_type_condition('number')
class NumberRangeFilter(FieldFilter):
    def get_query_range(self):
        min_value = self.filter_args.get("min")
        max_value = self.filter_args.get("max")
        return min_value, max_value

    def on_dicts(self, dicts):
        (min_value, max_value) = self.get_query_range()

        def is_value_matched(field_value):
            return (not min_value or field_value >= min_value) and \
                   (not max_value or field_value <= max_value)

        return [
            d for d in dicts
            if is_value_matched(d.get(self.field_name))
        ]
