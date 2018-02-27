from __future__ import absolute_import

from .base import FieldFilter
from .utils import is_same_class


class QueryFilter(object):
    filter_candidates = {}

    @classmethod
    def get_filter_key_from_type_and_condition(cls, filter_type,
                                               filter_condition):
        return "{}.{}".format(filter_type, filter_condition)

    @classmethod
    def register_type_condition(cls, filter_type, filter_condition):
        def decorator(filter_class):
            if not issubclass(filter_class, FieldFilter):
                raise "Filter to register must be a subclass of FieldFilter."
            filter_key = cls.get_filter_key_from_type_and_condition(
                filter_type, filter_condition)
            if filter_key in cls.filter_candidates and not is_same_class(
                    cls.filter_candidates[filter_key], filter_class
            ):
                raise ValueError(
                    "'{}' register failed, filter_key {} already owned by "
                    "other filter class({}).".format(
                        filter_class.__name__, filter_key,
                        cls.filter_candidates[filter_key].__name__)
                )
            else:  # Avoid override the same key cause hard to debug
                cls.filter_candidates[filter_key] = filter_class
            return filter_class

        return decorator

    def __init__(self, filter_dict):
        def _get_filter_from_filter_query_data(data):
            filter_key = self.get_filter_key_from_type_and_condition(
                data["type"], data["condition"]
            )

            if filter_key not in self.filter_candidates:
                raise KeyError("Filter {} does not registered.".format(
                    filter_key)
                )
            filter_cls = self.filter_candidates[filter_key]
            return filter_cls  # clarify the returning

        self.filters = [
            _get_filter_from_filter_query_data(query_data)(
                field_name, query_data
            )
            for (field_name, query_data) in filter_dict.items()
        ]

    def on_django_query(self, query):
        for filter_instance in self.filters:
            query = filter_instance.on_django_query(query)
        return query

    def on_sqlalchemy_query(self, query):
        for filter_instance in self.filters:
            query = filter_instance.on_sqlalchemy_query(query)
        return query

    def on_dicts(self, dicts):
        for filter_instance in self.filters:
            dicts = filter_instance.on_dicts(dicts)
        return dicts
