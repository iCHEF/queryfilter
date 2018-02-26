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

    @classmethod
    def _get_key_from_filter_query_data(cls, filter_query_data):
        filter_type = filter_query_data["type"]
        filter_condition = filter_query_data["condition"]
        return cls.get_filter_key_from_type_and_condition(
            filter_type, filter_condition)

    def __init__(self, filter_dict):
        try:
            self.filters = [
                self.filter_candidates[self._get_key_from_filter_query_data(
                    filter_query_data)](field_name, filter_query_data)
                for (field_name, filter_query_data) in filter_dict.items()
            ]
        except KeyError as missing_filter_key:
            raise KeyError("Filter {} does not registered.".format(
                missing_filter_key)
            )

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
