from __future__ import absolute_import

from .base import FieldFilter


class QueryFilter(object):
    filters_mapping = {}

    @classmethod
    def get_filter_key(cls, filter_type, filter_condition):
        return "{}.{}".format(filter_type, filter_condition)

    @classmethod
    def register_type_condition(cls, filter_type, filter_condition=None):
        def is_same_class(x_cls, y_cls):
            """
            Simply use "is" to compare two classes will not work,
            `cause class statement is an executable statement in python.

            So we'll need a customized comparing function.
            """
            full_path_of_x = x_cls.__module__ + "." + x_cls.__name__
            full_path_of_y = y_cls.__module__ + "." + y_cls.__name__
            return full_path_of_x == full_path_of_y

        def decorator(filter_class):
            if not issubclass(filter_class, FieldFilter):
                raise "Filter to register must be a subclass of FieldFilter."
            filter_key = cls.get_filter_key(filter_type, filter_condition)
            if filter_key in cls.filters_mapping and not is_same_class(
                    cls.filters_mapping[filter_key], filter_class
            ):
                raise ValueError(
                    "'{}' register failed, filter_key {} already owned by "
                    "other filter class({}).".format(
                        filter_class.__name__, filter_key,
                        cls.filters_mapping[filter_key].__name__)
                )
            else:  # Avoid override the same key cause hard to debug
                cls.filters_mapping[filter_key] = filter_class
            return filter_class

        return decorator

    def __init__(self, filter_dict):
        def _get_filter_cls_from_filter_query_data(data):
            filter_key = self.get_filter_key(
                data["type"], data.get("condition"))
            if filter_key not in self.filters_mapping:
                raise KeyError("Filter {} does not registered.".format(
                    filter_key)
                )
            filter_cls = self.filters_mapping[filter_key]
            return filter_cls  # clarify the returning

        self.filters = []
        for (field_name, query_data) in filter_dict.items():
            filter_cls = _get_filter_cls_from_filter_query_data(query_data)
            filter_options = query_data.get("options", {})
            filter_obj = filter_cls(
                field_name, query_data, options=filter_options)
            self.filters.append(filter_obj)

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
