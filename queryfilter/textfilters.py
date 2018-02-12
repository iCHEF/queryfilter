from __future__ import absolute_import

from .base import FieldFilter


class TextFullyMatchedFilter(FieldFilter):
    filter_type = "string"
    filter_condition = "equals"

    def on_dicts(self, dicts):
        return [
            d for d in dicts
            if bool(d.get(self.field_name) == self.filter_args["value"])
        ]
