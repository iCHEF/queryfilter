from __future__ import absolute_import

import pytest

from ..queryfilter import QueryFilter
from ..exceptions import (
    FilterOnNoneValueError,
    FieldNotFound
)
from .. import textfilters
from .. import numberfilters


class TestTextFilter(object):
    def test_simple_query_filter(self):
        dicts = [{"name": "name_example"}]
        query_filter = QueryFilter({
            "name": {
                "type": "string",
                "condition": "contains",
                "value": "example"
            }
        })
        assert len(query_filter.on_dicts(dicts)) == 1

    def test_simple_query_filter_with_field_not_found(self):
        dicts = [{"address": "address_example"}]
        query_filter = QueryFilter({
            "name": {
                "type": "string",
                "condition": "contains",
                "value": "example"
            }
        })
        assert len(query_filter.on_dicts(dicts)) == 0

    def test_True_drop_none_should_get_no_none_results(self):
        dicts = [
            {"age": None},
            {"age": 1},
            {"age": None},
            {"age": 2},
        ]
        query_filter = QueryFilter({
            "age": {
                "type": "number",
                "options": {"drop_none": True},
                "min": 0,
                "max": 1,
            }
        })
        assert len(query_filter.on_dicts(dicts)) == 1

    def test_False_drop_none_should_raise_FilterOnNoneValueError(self):
        dicts = [
            {"age": None},
            {"age": 1},
            {"age": None},
            {"age": 2}
        ]
        query_filter = QueryFilter({
            "age": {
                "type": "number",
                "options": {"drop_none": False},
                "min": 0,
                "max": 1
            }
        })
        with pytest.raises(FilterOnNoneValueError):
            query_filter.on_dicts(dicts)
