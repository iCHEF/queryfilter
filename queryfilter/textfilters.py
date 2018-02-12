from __future__ import absolute_import

from .base import FieldFilter


class TextFullyMatchedFilter(FieldFilter):
    filter_type = "string"
    filter_condition = "equals"

    def on_dicts(self, dicts):
        return [
            v for v in dicts
            if bool(dicts.get(self.field_name) == self.filter_args["value"])
        ]
