from queryfilter.filters import FieldFilter


class TextFullyMatchedFilter(FieldFilter):
    def __init__(self, field_name, match_target):
        self.match_target = match_target
        super(FieldFilter, self).__init__(field_name)

    @classmethod
    def get_filter_type(cls):
        return "string"

    @classmethod
    def get_filter_condition(cls):
        return "equals"

    def apply_to_django_query(self, query):
        return query.filter(**{self.field_name: self.match_target})

    def apply_to_sqlalchemy_query(self, query):
        return query.filter(**{self.field_name: self.match_target})

    def validate_object(self, object_to_validate):
        return bool(
            object_to_validate.get(self.field_name) == self.match_target)
