from __future__ import absolute_import

from queryfilter.tests.base_test_case import FilterTestCaseBase
from ..selectfilters import SelectFilter
from test_app.models import Data


FIELD_NAME = "type"


class TestSelectFilter(FilterTestCaseBase):

    def get_default_data(self):
        return [
            {FIELD_NAME: 1}
        ]

    @property
    def model_class(self):
        return Data

    def test_value_is_selected(self):

        choices = [1]

        text_filter = SelectFilter(FIELD_NAME, {
            "values": choices
        })

        self.assert_filtered_data_length(text_filter, 1)

    def test_value_is_one_of_selections(self):

        choices = [1, 2, 3, 4]

        text_filter = SelectFilter(FIELD_NAME, {
            "values": choices
        })

        self.assert_filtered_data_length(text_filter, 1)

    def test_value_not_selected(self):

        choices = [2, 3, 4]

        text_filter = SelectFilter(FIELD_NAME, {
            "values": choices
        })

        self.assert_filtered_data_length(text_filter, 0)

    def test_nothing_been_selected(self):

        text_filter = SelectFilter(FIELD_NAME, {
            "values": []
        })

        self.assert_filtered_data_length(text_filter, 0)

    def test_nothing_been_passed_to_filter(self):
        text_filter = SelectFilter(FIELD_NAME, {})

        self.assert_filtered_data_length(text_filter, 0)
