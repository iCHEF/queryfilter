from __future__ import absolute_import

from queryfilter.tests.base_test_case import FilterTestCaseBase
from test_app.models import Data
from ..textfilters import (
    TextFullyMatchedFilter, TextPartialMatchedFilter,
    TextStartsWithMatchedFilter, TextEndsWithMatchedFilter
)


class TextFilterTestBase(FilterTestCaseBase):

    field_name_to_test = "name"
    text_to_test = "name_example"

    @property
    def model_class(self):
        return Data

    def get_default_data(self):
        return [
            {self.field_name_to_test: self.text_to_test}
        ]


class TestTextFullyMatchedFilter(TextFilterTestBase):

    def test_text_fully_match(self):

        text_filter = TextFullyMatchedFilter(self.field_name_to_test, {
            "value": self.text_to_test
        })

        self.assert_filtered_data_length(text_filter, 1)

    def test_text_does_not_fully_match_should_fail(self):

        text_not_match = "not_name_example"
        text_filter = TextFullyMatchedFilter(self.field_name_to_test, {
            "value": text_not_match
        })

        self.assert_filtered_data_length(text_filter, 0)


class TestTextPartialMatchedFilter(TextFilterTestBase):
    def test_text_partial_match(self):
        text_filter = TextPartialMatchedFilter(self.field_name_to_test, {
            "value": self.text_to_test[:1]
        })
        self.assert_filtered_data_length(text_filter, 1)

    def test_text_does_not_partial_match_should_fail(self):

        text_not_match = "not"
        text_filter = TextPartialMatchedFilter(self.field_name_to_test, {
            "value": text_not_match
        })

        self.assert_filtered_data_length(text_filter, 0)


class TestTextStartsWithMatchedFilter(TextFilterTestBase):
    def test_text_partial_match(self):

        text_filter = TextStartsWithMatchedFilter(self.field_name_to_test, {
            "value": self.text_to_test[:1]
        })

        self.assert_filtered_data_length(text_filter, 1)

    def test_text_does_not_partial_match_should_fail(self):

        text_not_match = "not"
        text_filter = TextStartsWithMatchedFilter(self.field_name_to_test, {
            "value": text_not_match
        })
        self.assert_filtered_data_length(text_filter, 0)

        text_not_match_with_endwith = self.text_to_test[-1:]
        text_filter = TextStartsWithMatchedFilter(self.field_name_to_test, {
            "value": text_not_match_with_endwith
        })
        self.assert_filtered_data_length(text_filter, 0)


class TestTextEndsWithMatchedFilter(TextFilterTestBase):
    def test_text_partial_match(self):
        text_filter = TextEndsWithMatchedFilter(self.field_name_to_test, {
            "value": self.text_to_test[-1:]
        })
        self.assert_filtered_data_length(text_filter, 1)

    def test_text_does_not_partial_match_should_fail(self):
        text_not_match = "not"
        text_filter = TextEndsWithMatchedFilter(self.field_name_to_test, {
            "value": text_not_match
        })
        self.assert_filtered_data_length(text_filter, 0)

        text_not_match_with_startwith = self.text_to_test[:1]
        text_filter = TextEndsWithMatchedFilter(self.field_name_to_test, {
            "value": text_not_match_with_startwith
        })
        self.assert_filtered_data_length(text_filter, 0)
