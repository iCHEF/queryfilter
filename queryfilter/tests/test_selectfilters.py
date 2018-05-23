from __future__ import absolute_import
import pytest
from ..selectfilters import SelectFilter
from test_app.models import Data


FIELD_NAME = "type"


@pytest.mark.django_db(transaction=True)
class TestSelectFilter(object):

    def setup(self):

        self.dicts = [
            {FIELD_NAME: 1}
        ]

        self.queryset = self._save_to_db(self.dicts)

    def _save_to_db(self, data):

        for datum in data:
            Data.objects.create(**datum)

        return Data.objects.all()

    def _assert_filtered_data_length(self, filter, length):
        
        assert len(filter.on_dicts(self.dicts)) == length
        assert len(filter.on_django_query(self.queryset)) == length

    def test_value_is_selected(self):

        choices = [1]

        text_filter = SelectFilter(FIELD_NAME, {
            "values": choices
        })

        self._assert_filtered_data_length(text_filter, 1)

    def test_value_is_one_of_selections(self):

        choices = [1, 2, 3, 4]

        text_filter = SelectFilter(FIELD_NAME, {
            "values": choices
        })

        self._assert_filtered_data_length(text_filter, 1)

    def test_value_not_selected(self):

        choices = [2, 3, 4]

        text_filter = SelectFilter(FIELD_NAME, {
            "values": choices
        })

        self._assert_filtered_data_length(text_filter, 0)

    def test_nothing_been_selected(self):
        
        text_filter = SelectFilter(FIELD_NAME, {
            "values": []
        })

        self._assert_filtered_data_length(text_filter, 0)

    def test_nothing_been_passed_to_filter(self):
        text_filter = SelectFilter(FIELD_NAME, {})
        
        self._assert_filtered_data_length(text_filter, 0)
