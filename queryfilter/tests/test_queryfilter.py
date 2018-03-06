from __future__ import absolute_import

import pytest

from ..queryfilter import QueryFilter
from ..exceptions import (
    FilterOnNoneValue,
    FieldNotFound
)


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
                "options": {"none_for_missing_field": False},
                "condition": "contains",
                "value": "example"
            }
        })
        with pytest.raises(FieldNotFound):
            query_filter.on_dicts(dicts)

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

    def est_False_drop_none_should_raise_FilterOnNoneValue(self):
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
        with pytest.raises(FilterOnNoneValue):
            query_filter.on_dicts(dicts)
