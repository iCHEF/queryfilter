from __future__ import absolute_import

from .base import FieldFilter, DictFilterMixin
from .queryfilter import QueryFilter


@QueryFilter.register_type_condition('number')
class NumberRangeFilter(DictFilterMixin, FieldFilter):
    def get_query_range(self):
        min_value = self.filter_args.get("min")
        max_value = self.filter_args.get("max")
        return min_value, max_value

    def on_dicts(self, dicts):
        (min_value, max_value) = self.get_query_range()

        def is_value_matched(field_value):
            if field_value is None:
                return self.false_with_drop_none_else_raise(self.field_name)

            return (min_value is None or field_value >= min_value) and \
                   (max_value is None or field_value <= max_value)

        return [
            d for d in dicts
            if is_value_matched(self.get(d, self.field_name))
        ]
