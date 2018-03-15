from __future__ import absolute_import

import pytest

from ..exceptions import (
    FieldNotFound
)
from ..textfilters import (
    TextFullyMatchedFilter
)


class TestNestedFiler(object):
    def setup(self):
        self.field_name_to_test = "user__name"
        self.text_to_test = "name_example"
        self.dicts = [
            {
                "user": {
                    "name": self.text_to_test
                }
            }
        ]

    def test_text_fully_match(self):
        text_filter = TextFullyMatchedFilter(self.field_name_to_test, {
            "value": self.text_to_test
        })
        assert len(text_filter.on_dicts(self.dicts)) == 1

    def test_text_does_not_match_should_get_nothing_back(self):
        text_not_match = "not_name_example"
        text_filter = TextFullyMatchedFilter(self.field_name_to_test, {
            "value": text_not_match
        })
        assert len(text_filter.on_dicts(self.dicts)) == 0

    def test_none_as_value_should_work_as_well(self):
        text_filter = TextFullyMatchedFilter(self.field_name_to_test, {
            "value": None
        })
        assert len(text_filter.on_dicts(self.dicts)) == 0

    def test_key_not_exist_should_work_as_well(self):
        text_filter = TextFullyMatchedFilter(self.field_name_to_test, {
            "value": self.text_to_test
        })
        assert len(text_filter.on_dicts({})) == 0

    def test_key_not_exist_should_raise_with_option(self):
        text_filter = TextFullyMatchedFilter(self.field_name_to_test, {
            "value": self.text_to_test,
        }, options={"none_for_missing_field": False})
        with pytest.raises(FieldNotFound):
            text_filter.on_dicts([{}])
