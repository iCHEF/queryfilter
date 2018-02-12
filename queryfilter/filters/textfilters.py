from queryfilter.filters import FieldFilter


class TextFullyMatchedFilter(FieldFilter):
    filter_type = "string"
    filter_condition = "equals"

    def __init__(self, field_name, match_target):
        self.match_target = match_target
        super(FieldFilter, self).__init__(field_name)

    def on_instance(self, object_to_validate):
        return bool(
            object_to_validate.get(self.field_name) == self.match_target)
