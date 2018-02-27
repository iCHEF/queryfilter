from __future__ import absolute_import

from ..numberfilters import NumberRangeFilter


class TestNumberRangeFilter(object):
    def setup(self):
        self.field_name_to_test = "age"
        self.number_to_test = 5
        self.dicts = [
            {self.field_name_to_test: self.number_to_test}
        ]

    def test_number_in_range(self):
        text_filter = NumberRangeFilter(self.field_name_to_test, {
            "max": self.number_to_test+1, "min": self.number_to_test-1
        })
        assert len(text_filter.on_dicts(self.dicts)) == 1

    def test_number_out_of_range_too_small(self):
        text_filter = NumberRangeFilter(self.field_name_to_test, {
            "max": self.number_to_test+1, "min": self.number_to_test+1
        })
        assert len(text_filter.on_dicts(self.dicts)) == 0

    def test_number_out_of_range_too_big(self):
        text_filter = NumberRangeFilter(self.field_name_to_test, {
            "max": self.number_to_test-1, "min": self.number_to_test-1
        })
        assert len(text_filter.on_dicts(self.dicts)) == 0

    def test_number_right_on_range(self):
        text_filter = NumberRangeFilter(self.field_name_to_test, {
            "max": self.number_to_test, "min": self.number_to_test
        })
        assert len(text_filter.on_dicts(self.dicts)) == 1

    def test_number_has_no_range(self):
        text_filter = NumberRangeFilter(self.field_name_to_test, {})
        assert len(text_filter.on_dicts(self.dicts)) == 1

    def test_number_under_max(self):
        text_filter = NumberRangeFilter(self.field_name_to_test, {
            "max": self.number_to_test+1
        })
        assert len(text_filter.on_dicts(self.dicts)) == 1

    def test_number_over_max(self):
        text_filter = NumberRangeFilter(self.field_name_to_test, {
            "max": self.number_to_test-1
        })
        assert len(text_filter.on_dicts(self.dicts)) == 0

    def test_number_at_max(self):
        text_filter = NumberRangeFilter(self.field_name_to_test, {
            "max": self.number_to_test
        })
        assert len(text_filter.on_dicts(self.dicts)) == 1

    def test_number_under_min(self):
        text_filter = NumberRangeFilter(self.field_name_to_test, {
            "min": self.number_to_test+1
        })
        assert len(text_filter.on_dicts(self.dicts)) == 0

    def test_number_over_min(self):
        text_filter = NumberRangeFilter(self.field_name_to_test, {
            "min": self.number_to_test-1
        })
        assert len(text_filter.on_dicts(self.dicts)) == 1

    def test_number_at_min(self):
        text_filter = NumberRangeFilter(self.field_name_to_test, {
            "min": self.number_to_test
        })
        assert len(text_filter.on_dicts(self.dicts)) == 1
