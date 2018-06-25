import graphene

TYPE_FIELD_DESC = "Don't modify if you're not using customized filter"


class TextFilterTypes(graphene.Enum):
    EQUALS = 'equals'
    CONTAINS = 'contains'
    STARTS_WITH = 'starts_with'
    ENDS_WITH = 'ends_with'


class BirthdayFilterTypes(graphene.Enum):
    DATE_RANGE = 'date_range'


class TextFilterQueryType(graphene.InputObjectType):
    type = graphene.String(
        default_value="string",
        description=TYPE_FIELD_DESC
    )
    condition = graphene.Field(
        TextFilterTypes, default_value=TextFilterTypes.EQUALS.value
    )
    value = graphene.String(description="text to query")


class SelectStringFilterQueryType(graphene.InputObjectType):

    type = graphene.String(
        default_value="select",
        description=TYPE_FIELD_DESC
    )

    values = graphene.List(
        graphene.String, description="text list to query"
    )


class SelectFloatFilterQueryType(graphene.InputObjectType):

    type = graphene.String(
        default_value="select",
        description=TYPE_FIELD_DESC
    )

    values = graphene.List(
        graphene.Float, description="number list to query", required=True
    )


class NumberRangeFilterQueryType(graphene.InputObjectType):
    type = graphene.String(
        default_value="number",
        description=TYPE_FIELD_DESC
    )
    min = graphene.Float()
    max = graphene.Float()

    @property
    def invalid_message(self):
        return self.id.startswith('userid_')


class BirthFilterQueryType(graphene.InputObjectType):
    type = graphene.String(
        default_value="birthday",
        description=TYPE_FIELD_DESC
    )
    condition = graphene.Field(
        BirthdayFilterTypes, default_value=BirthdayFilterTypes.DATE_RANGE.value
    )
    start = graphene.String(default="01/01")
    end = graphene.String(default="12/31")


class DatetimeRangeFilterType(graphene.InputObjectType):
    type = graphene.String(
        default_value="datetime",
        description=TYPE_FIELD_DESC
    )
    start = graphene.String()
    end = graphene.String()
