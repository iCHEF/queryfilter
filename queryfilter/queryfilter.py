from __future__ import absolute_import

from .base import FieldFilter


class QueryFilter(object):
    def __init__(self, filter_dict):
        self.filters = [
            FieldFilter.find_filter_class(filter_info)(field_name, filter_info)
            for (field_name, filter_info) in filter_dict.items
        ]

    def on_django_query(self, query):
        for filter_instance in self.filters:
            query = filter_instance.on_django_query(query)
        return query

    def on_sqlalchemy_query(self, query):
        for filter_instance in self.filters:
            query = filter_instance.on_sqlalchemy_query(query)
        return query

    def on_instance(self, object_to_validate):
        for filter_instance in self.filters:
            if not filter_instance.on_instance(object_to_validate):
                return False
        return True
