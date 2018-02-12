import abc


class FieldFilter(object):
    __metaclass__ = abc.ABCMeta

    @classmethod
    def find_filter_class(cls, filter_info):
        """
        filter_info example:
        "name": {
            "type": "string",
            "condition": "contains",
            "query": "Alex",
        },
        """
        filter_type = filter_info["type"]
        filter_condition = filter_info["condition"]
        for filter_cls in cls.__subclasses__():
            if filter_cls.filter_type == filter_type and \
                            filter_cls.filter_condition == filter_condition:
                return filter_cls
        raise NotImplementedError(
            "Type: {0} and condition: {1} doesn't exist.".format())

    def __init__(self, field_name):
        self.field_name = field_name

    @abc.abstractmethod
    def apply_to_django_query(self, query):
        pass

    @abc.abstractmethod
    def apply_to_sqlalchemy_query(self, query):
        pass

    @abc.abstractmethod
    def validate_object(self, object_to_validate):
        pass
