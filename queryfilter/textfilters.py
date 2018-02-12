from __future__ import absolute_import

from .base import FieldFilter


class TextFullyMatchedFilter(FieldFilter):
    filter_type = "string"
    filter_condition = "equals"

    def on_instance(self, instance):
        return bool(instance.get(self.field_name) == self.filter_args["value"])
