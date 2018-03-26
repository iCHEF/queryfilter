import graphene

from queryfilter import QueryFilter

from queryfilter.schema import (
    TextFilterQueryObject,
    NumberRangeFilterQueryObject,
    SelectFloatFilterQueryObject
)

EXAMPLE_DATA = [{
    "name": "A",
    "price": 100,
    "type": 0
}, {
    "name": "B",
    "price": 5,
    "type": 1
}]


class ExampleDataSchema(graphene.ObjectType):
    name = graphene.String()
    price = graphene.Float()
    type = graphene.Float()

    def resolve_name(self, info):
        return self.get("name")

    def resolve_price(self, info):
        return self.get("price")

    def resolve_type(self, info):
        return self.get("type")


class ExampleQueryFilter(graphene.InputObjectType):
    name = TextFilterQueryObject()
    price = NumberRangeFilterQueryObject()
    type = SelectFloatFilterQueryObject()


class ExampleSchemaWithFilter(graphene.ObjectType):
    something = graphene.List(
        ExampleDataSchema, queryFilter=ExampleQueryFilter())

    def resolve_something(self, info, **kwargs):
        query_filter = kwargs.get('queryFilter', {})
        query_filter = QueryFilter(query_filter)
        examples = query_filter.on_dicts(EXAMPLE_DATA)
        return examples


example_schema = graphene.Schema(query=ExampleSchemaWithFilter)
