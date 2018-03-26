import graphene

from queryfilter import QueryFilter

from queryfilter.schema import (
    TextFilterQueryObject, NumberRangeFilterQueryObject,
    SelectFloatFilterQueryObject
)


class KeyCanBeAccessedAsAttributes(dict):
    """
    Allow graphene to access dict value directly. (xx.a instead of xx.get("a") or xx["a"])
    """
    def __init__(self, *args, **kwargs):
        super(KeyCanBeAccessedAsAttributes, self).__init__(*args, **kwargs)
        for arg in args:
            if isinstance(arg, dict):
                for k, v in arg.iteritems():
                    self[k] = v

        if kwargs:
            for k, v in kwargs.iteritems():
                self[k] = v

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        super(KeyCanBeAccessedAsAttributes, self).__setitem__(key, value)
        self.__dict__.update({key: value})

    def __delattr__(self, item):
        self.__delitem__(item)

    def __delitem__(self, key):
        super(KeyCanBeAccessedAsAttributes, self).__delitem__(key)
        del self.__dict__[key]


EXAMPLE_DATA = [
            KeyCanBeAccessedAsAttributes({
                "name": "A",
                "price": 100,
                "type": 0
            }),
            KeyCanBeAccessedAsAttributes({
                "name": "B",
                "price": 5,
                "type": 1
            }),
        ]


class ExampleDataSchema(graphene.ObjectType):
    name = graphene.String()
    price = graphene.Float()
    type = graphene.Float()


class ExampleQueryFilter(graphene.InputObjectType):
    name = TextFilterQueryObject()
    price = NumberRangeFilterQueryObject()
    type = SelectFloatFilterQueryObject()


class ExampleSchemaWithFilter(graphene.ObjectType):
    something = graphene.List(
        ExampleDataSchema, queryFilter=ExampleQueryFilter()
    )

    def resolve_something(self, info, **kwargs):
        query_filter = kwargs.get('queryFilter', {})
        query_filter = QueryFilter(query_filter)
        examples = query_filter.on_dicts(EXAMPLE_DATA)
        return examples


example_schema = graphene.Schema(query=ExampleSchemaWithFilter)
