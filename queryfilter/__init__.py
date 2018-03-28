from __future__ import absolute_import

from .queryfilter import QueryFilter  # noqa: imported as root level object

from .base import FieldFilter
from .textfilters import (
    TextFullyMatchedFilter, TextPartialMatchedFilter,
    TextStartsWithMatchedFilter, TextEndsWithMatchedFilter
)
from .selectfilters import SelectFilter
from .numberfilters import NumberRangeFilter
from .birthdayfilters import BirthdayDateRangeFilter

from .schemas import (
    TextFilterQueryType, NumberRangeFilterQueryType,
    SelectStringFilterQueryType, SelectFloatFilterQueryType,
    BirthFilterQueryType
)

__all__ = [
    # Main interface
    'QueryFilter',

    # Filter base class
    'FieldFilter',

    # Default filters
    'TextFullyMatchedFilter',
    'TextPartialMatchedFilter',
    'TextStartsWithMatchedFilter',
    'TextEndsWithMatchedFilter',
    'SelectFilter',
    'NumberRangeFilter',
    'BirthdayDateRangeFilter',

    # Default GraphQL schemas
    'TextFilterQueryType',
    'NumberRangeFilterQueryType',
    'SelectStringFilterQueryType',
    'SelectFloatFilterQueryType',
    'BirthFilterQueryType'
]
