from filters import FieldFilter


class FilterManager(object):
    def __init__(self, filter_dict):
        self.filters = [
            FieldFilter.find_filter_class(filter_info)(field_name, filter_info)
            for (field_name, filter_info) in filter_dict.items
        ]

    def add_filter(self, filter_instance):
        if not issubclass(filter_instance.cls, FieldFilter):
            raise TypeError("{0} is not a FieldFilter class.".format(
                filter_instance.cls.__name__))
        self.filters.append(filter_instance)

    def apply_to_django_query(self, query):
        for filter_instance in self.filters:
            query = filter_instance.apply_to_django_query(query)
        return query

    def apply_to_sqlalchemy_query(self, query):
        for filter_instance in self.filters:
            query = filter_instance.apply_to_sqlalchemy_query(query)
        return query

    def validate_object(self, object_to_validate):
        for filter_instance in self.filters:
            if not filter_instance.validate_object(object_to_validate):
                return False
        return True
