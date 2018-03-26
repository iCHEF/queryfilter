import graphene

from queryfilter import QueryFilter

from queryfilter.schema import (
    TextFilterQueryObject, NumberRangeFilterQueryObject,
    SelectFloatFilterQueryObject
)


class ExampleDataSchema(graphene.ObjectType):
    name = graphene.String()
    price = graphene.Float()
    type = graphene.Float()


class ExampleQueryFilter(graphene.ObjectType):
    name = TextFilterQueryObject()
    price = NumberRangeFilterQueryObject()
    type = SelectFloatFilterQueryObject()


class ExampleSchemaWithFilter(graphene.ObjectType):
    something = graphene.Field(
        ExampleDataSchema, name="example", queryFilter=ExampleQueryFilter()
    )

    def resolve_something(self, info, **kwargs):
        examples = []
        query_filter = kwargs.get('reportFilter', {})

        query_filter = QueryFilter(query_filter)
        examples = query_filter.on_dicts(examples)

        return examples
