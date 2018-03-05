from __future__ import absolute_import

from ..birthdayfilters import (
    BirthdayDateRangeFilter,
    BirthdayAgeRangeFilter
)


class TestBirthdayDateRangeFilter(object):

    def date_to_test(self, month_to_test=None, day_to_test=None):
        month_to_test = month_to_test or self.month_to_test
        day_to_test = day_to_test or self.day_to_test
        return month_to_test + "/" + day_to_test

    def values_of_filters(self, results):
        return [result[self.field_name_to_test] for result in results]

    def setup(self):
        self.field_name_to_test = "birth"
        self.dates_to_test = ("12/31", "01/11", "02/29", "01/11")
        self.dataset_to_test = [
            {self.field_name_to_test: date} for date in self.dates_to_test
        ]

    def test_date_matched_with_same_date_should_be_in_range(self):
        date_filter = BirthdayDateRangeFilter(self.field_name_to_test, {
            "start": self.dates_to_test[0],
            "end": self.dates_to_test[0]
        })
        results_after_filter = date_filter.on_dicts(self.dataset_to_test)
        assert len(results_after_filter) == 1

    def test_date_not_matched_with_same_date_should_not_be_in_range(self):
        date_not_matched = "12/30"
        assert date_not_matched not in self.dates_to_test
        date_filter = BirthdayDateRangeFilter(self.field_name_to_test, {
            "start": date_not_matched,
            "end": date_not_matched
        })
        results_after_filter = date_filter.on_dicts(self.dataset_to_test)
        assert len(results_after_filter) == 0

    def test_date_range_across_year_should_match(self):
        date_filter = BirthdayDateRangeFilter(self.field_name_to_test, {
            "start": "12/30",
            "end": "01/30",
        })
        results_after_filter = date_filter.on_dicts(self.dataset_to_test)
        assert len(results_after_filter) == 3
        values_of_result_filters = self.values_of_filters(results_after_filter)
        assert "12/31" in values_of_result_filters
        assert "01/11" in values_of_result_filters

    def test_date_range_not_across_year_should_match(self):
        date_filter = BirthdayDateRangeFilter(self.field_name_to_test, {
            "start": "01/30",
            "end": "12/30",
        })
        results_after_filter = date_filter.on_dicts(self.dataset_to_test)
        assert len(results_after_filter) == 1
        assert results_after_filter[0]["birth"] == "02/29"


class TestBirthdayAgeRangeFilter(object):

    def setup(self):
        self.field_name_to_test = "age"
        self.ages_to_test = ("14", "21", "99", "21")
        self.dataset_to_test = [
            {self.field_name_to_test: age} for age in self.ages_to_test
        ]

    def test_filter_with_exact_age_should_match_on_expected_amount(self):
        age_filter = BirthdayAgeRangeFilter(self.field_name_to_test, {
            "start": self.ages_to_test[0],
            "end": self.ages_to_test[0]
        })
        results_after_filter = age_filter.on_dicts(self.dataset_to_test)
        assert len(results_after_filter) == 1

    def test_filter_with_date_not_matched_should_get_empty_results(self):
        age_not_matched = "18"
        assert age_not_matched not in self.ages_to_test
        age_filter = BirthdayAgeRangeFilter(self.field_name_to_test, {
            "start": age_not_matched,
            "end": age_not_matched
        })
        results_after_filter = age_filter.on_dicts(self.dataset_to_test)
        assert len(results_after_filter) == 0

    def test_filter_with_date_range_all_covered_should_match_all(self):
        smallest_age_of_test_dataset = int(min(self.ages_to_test))
        largest_age_of_test_dataset = int(max(self.ages_to_test))
        date_filter = BirthdayAgeRangeFilter(self.field_name_to_test, {
            "start": str(smallest_age_of_test_dataset - 1),
            "end": str(largest_age_of_test_dataset + 1),
        })
        results_after_filter = date_filter.on_dicts(self.dataset_to_test)
        assert len(results_after_filter) == len(self.dataset_to_test)

    def test_date_range_across_year_should_match(self):
        smallest_age_of_test_dataset = int(min(self.ages_to_test))
        largest_age_of_test_dataset = int(max(self.ages_to_test))
        date_filter = BirthdayAgeRangeFilter(self.field_name_to_test, {
            "start": str(smallest_age_of_test_dataset + 1),
            "end": str(largest_age_of_test_dataset - 1),
        })
        results_after_filter = date_filter.on_dicts(self.dataset_to_test)
        assert len(results_after_filter) == (len(self.dataset_to_test) - 2)
