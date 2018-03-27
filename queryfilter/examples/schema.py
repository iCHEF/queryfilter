import graphene

from queryfilter import QueryFilter

from queryfilter.schemas import (
    TextFilterQueryType,
    NumberRangeFilterQueryType,
    SelectFloatFilterQueryType,
    SelectStringFilterQueryType,
    BirthFilterQueryType
)

EXAMPLE_DATA = [{
    "name": "A",
    "price": 100,
    "type": 0,
    "category": "X",
    "birthday": "05/20"
}, {
    "name": "B",
    "price": 5,
    "type": 1,
    "category": "Y",
    "birthday": "12/20"
}]


class ExampleDataSchema(graphene.ObjectType):
    name = graphene.String()
    price = graphene.Float()
    type = graphene.Float()
    category = graphene.String()
    birthday = graphene.String()

    def resolve_name(self, info):
        return self.get("name")

    def resolve_price(self, info):
        return self.get("price")

    def resolve_type(self, info):
        return self.get("type")

    def resolve_category(self, info):
        return self.get("category")

    def resolve_birthday(self, info):
        return self.get("birthday")


class ExampleQueryFilter(graphene.InputObjectType):
    name = TextFilterQueryType()
    price = NumberRangeFilterQueryType()
    type = SelectFloatFilterQueryType()
    category = SelectStringFilterQueryType()
    birthday = BirthFilterQueryType()


class ExampleSchemaWithFilter(graphene.ObjectType):
    something = graphene.List(
        ExampleDataSchema, queryFilter=ExampleQueryFilter())

    def resolve_something(self, info, **kwargs):
        query_filter = kwargs.get('queryFilter', {})
        query_filter = QueryFilter(query_filter)
        examples = query_filter.on_dicts(EXAMPLE_DATA)
        return examples


example_schema = graphene.Schema(query=ExampleSchemaWithFilter)
