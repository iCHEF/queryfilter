from __future__ import absolute_import

import pytest

from ..numberfilters import NumberRangeFilter


class TestNumberRangeFilter(object):
    def setup(self):
        self.field_name_to_test = "age"
        self.numbers_to_test = (0, 3, None, 2, 2, 4)
        self.dicts = [
            {self.field_name_to_test: num}
            for num in self.numbers_to_test
        ]

    @property
    def max_test_number(self):
        no_none_values = (
            d[self.field_name_to_test] for d in self.no_none_test_numbers
        )
        return max(no_none_values)

    @property
    def min_test_number(self):
        no_none_values = (
            d[self.field_name_to_test] for d in self.no_none_test_numbers
        )
        return min(no_none_values)

    @property
    def no_none_test_numbers(self):
        return filter(
            lambda d: d[self.field_name_to_test] is not None, self.dicts
        )

    def test_filter_range_cover_all_tesT_numbers_should_get_same_numbers(self):
        text_filter = NumberRangeFilter(self.field_name_to_test, {
            "max": self.max_test_number + 1, "min": self.min_test_number - 1
        })
        filtered_dicts = text_filter.on_dicts(self.dicts)
        assert len(filtered_dicts) == len(list(self.no_none_test_numbers))

    def test_range_smaller_than_test_numbers_should_get_empty_list(self):
        text_filter = NumberRangeFilter(self.field_name_to_test, {
            "max": self.min_test_number - 1, "min": self.min_test_number - 1
        })
        assert len(text_filter.on_dicts(self.dicts)) == 0

    def test_range_larger_than_test_numbers_should_get_empty_list(self):
        text_filter = NumberRangeFilter(self.field_name_to_test, {
            "max": self.max_test_number + 1, "min": self.max_test_number + 1
        })
        assert len(text_filter.on_dicts(self.dicts)) == 0

    def test_range_with_0_should_get_result(self):
        text_filter = NumberRangeFilter(self.field_name_to_test, {
            "max": 0, "min": 0
        })
        assert len(text_filter.on_dicts(self.dicts)) == 1

    def test_number_has_no_range(self):
        text_filter = NumberRangeFilter(self.field_name_to_test, {})
        filtered_dicts = text_filter.on_dicts(self.dicts)
        assert len(filtered_dicts) == len(list(self.no_none_test_numbers))

    def test_range_with_smaller_max_option_only(self):
        text_filter = NumberRangeFilter(self.field_name_to_test, {
            "max": self.max_test_number - 1
        })
        filtered_dicts = text_filter.on_dicts(self.dicts)
        assert len(filtered_dicts) == len(list(self.no_none_test_numbers)) - 1

    @pytest.mark.parametrize("max_bias", [1, 0])
    def test_range_with_larger_or_equal_max_option_only(self, max_bias):
        text_filter = NumberRangeFilter(self.field_name_to_test, {
            "max": self.max_test_number + max_bias
        })
        filtered_dicts = text_filter.on_dicts(self.dicts)
        assert len(filtered_dicts) == len(list(self.no_none_test_numbers))

    def test_range_with_larger_min_option_only(self):
        text_filter = NumberRangeFilter(self.field_name_to_test, {
            "min": self.min_test_number + 1
        })
        filtered_dicts = text_filter.on_dicts(self.dicts)
        assert len(filtered_dicts) == len(list(self.no_none_test_numbers)) - 1

    @pytest.mark.parametrize("min_bias", [1, 0])
    def test_range_with_smaller_or_equal_min_option_only(self, min_bias):
        text_filter = NumberRangeFilter(self.field_name_to_test, {
            "min": self.min_test_number - min_bias
        })
        filtered_dicts = text_filter.on_dicts(self.dicts)
        assert len(filtered_dicts) == len(list(self.no_none_test_numbers))
