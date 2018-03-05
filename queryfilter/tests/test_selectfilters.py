from __future__ import absolute_import

from ..selectfilters import SelectFilter


class TestSelectFilter(object):
    def setup(self):
        self.field_name_to_test = "member_type"
        self.type_to_test = 1
        self.dicts = [
            {self.field_name_to_test: self.type_to_test}
        ]

    def test_value_is_selected(self):
        text_filter = SelectFilter(self.field_name_to_test, {
            "values": [self.type_to_test]
        })
        assert len(text_filter.on_dicts(self.dicts)) == 1

    def test_value_is_one_of_selections(self):
        text_filter = SelectFilter(self.field_name_to_test, {
            "values": [self.type_to_test, 2, 3, 4]
        })
        assert len(text_filter.on_dicts(self.dicts)) == 1

    def test_value_not_selected(self):
        text_filter = SelectFilter(self.field_name_to_test, {
            "values": [2, 3, 4]
        })
        assert len(text_filter.on_dicts(self.dicts)) == 0

    def test_nothing_been_selected(self):
        text_filter = SelectFilter(self.field_name_to_test, {
            "values": []
        })
        assert len(text_filter.on_dicts(self.dicts)) == 0

    def test_nothing_been_passed_to_filter(self):
        text_filter = SelectFilter(self.field_name_to_test, {})
        assert len(text_filter.on_dicts(self.dicts)) == 0
