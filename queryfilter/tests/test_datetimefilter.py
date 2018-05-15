from __future__ import absolute_import

import pytest
from ..datetimefilter import DateRangeFilter


ordered_triple_test_date_set = (
    ("2016-12-29T00:00:00+08:00", "2016-12-30T00:00:00+08:0", "2016-12-31T00:00:00+08:0"),  # in three day
    ("2016-12-31T00:00:00+08:00", "2016-12-31T01:00:00+08:0", "2016-12-31T02:00:00+08:0"),  # in one day
    ("2016-12-31T00:00:00+08:00", "2017-12-31T01:00:00+08:0", "2018-12-31T02:00:00+08:0"),  # across year
)

date_time_parametrize = pytest.mark.parametrize("dates, test_data",
                                                zip(ordered_triple_test_date_set, ordered_triple_test_date_set),
                                                indirect=['test_data'])


@pytest.fixture
def test_data(request):
    return [{FIELD_NAME: date} for date in request.param]


FIELD_NAME = 'datetime'


class TestDateRangeFilter(object):

    @date_time_parametrize
    def test_out_of_range(self, dates, test_data):

        date = dates[0]
        date = "1990" + date[4:]

        date_filter = DateRangeFilter(FIELD_NAME, {
            "start": date,
            "end": date,
        })
        results_after_filter = date_filter.on_dicts(test_data)
        assert len(results_after_filter) == 0

    @date_time_parametrize
    def test_date_matched_with_only_one_time_point(self, dates, test_data):

        date = dates[1]

        date_filter = DateRangeFilter(FIELD_NAME, {
            "start": date,
            "end": date,
        })
        results_after_filter = date_filter.on_dicts(test_data)
        assert len(results_after_filter) == 1

    @date_time_parametrize
    def test_missing_start_or_end(self, dates, test_data):

        date = dates[1]

        date_filter = DateRangeFilter(FIELD_NAME, {
            "start": date,
        })

        results_after_filter = date_filter.on_dicts(test_data)
        assert len(results_after_filter) == 2

        date_filter = DateRangeFilter(FIELD_NAME, {
            "end": date,
        })
        results_after_filter = date_filter.on_dicts(test_data)
        assert len(results_after_filter) == 2
