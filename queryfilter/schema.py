import graphene

TYPE_FIELD_DESC = "Don't modify if you're not using customized filter"


class TextFilterType(graphene.Enum):
    EQUALS = 'equals'
    CONTAINS = 'contains'
    STARTS_WITH = 'starts_with'
    ENDS_WITH = 'ends_with'


class TextFilterQueryObject(graphene.InputObjectType):
    type = graphene.String(
        default_value="string",
        description=TYPE_FIELD_DESC
    )
    condition = graphene.Field(
        TextFilterType, default_value=TextFilterType.EQUALS.value
    )
    value = graphene.String(description="text to query", required=True)


class SelectStringFilterQueryObject(graphene.InputObjectType):

    type = graphene.String(
        default_value="select",
        description=TYPE_FIELD_DESC
    )

    values = graphene.List(
        graphene.String, description="text list to query", required=True
    )


class SelectFloatFilterQueryObject(graphene.InputObjectType):

    type = graphene.String(
        default_value="select",
        description=TYPE_FIELD_DESC
    )

    values = graphene.List(
        graphene.Float, description="number list to query", required=True
    )


class NumberRangeFilterQueryObject(graphene.InputObjectType):
    type = graphene.String(
        default_value="number",
        description=TYPE_FIELD_DESC
    )
    min = graphene.Float()
    max = graphene.Float()

    @property
    def invalid_message(self):
        return self.id.startswith('userid_')


class BirthFilterQueryObject(graphene.InputObjectType):
    type = graphene.String(
        default_value="birthday",
        description=TYPE_FIELD_DESC
    )
    start = graphene.String(default="01/01")
    end = graphene.String(default="12/31")
