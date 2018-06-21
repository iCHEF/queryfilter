from __future__ import absolute_import

import pytest
import dateutil.parser
from test_app.models import DatetimeFilterTestingModel
from ..datetimefilter import DatetimeRangeFilter


# they are designed to be strictly ordered and used for testing
ordered_triple_test_date_set = (

    (   # in three day
        "2016-12-29T00:00:00+08:00",
        "2016-12-30T00:00:00+08:00",
        "2016-12-31T00:00:00+08:00"
    ),
    (   # in one day
        "2016-12-31T00:00:00+08:00",
        "2016-12-31T01:00:00+08:0",
        "2016-12-31T02:00:00+08:00"
    ),
    (   # across year
        "2016-12-31T23:00:00+08:00",
        "2017-01-01T00:00:00-08:00",
        "2018-12-31T02:00:00+08:00"
    ),
    (   # no time zone
        "2016-12-31T23:00:00",
        "2017-01-01T00:00:00",
        "2018-12-31T02:00:00"
    ),
    (   # date only
        "2016-12-31",
        "2017-01-01",
        "2018-12-31"
    ),
)


parametrization_data = zip(ordered_triple_test_date_set,
                           ordered_triple_test_date_set,
                           ordered_triple_test_date_set,
                           )

date_time_parametrize = pytest.mark.parametrize(
    "dates, test_data, queryset",
    parametrization_data,
    indirect=['test_data', 'queryset']
)


@pytest.fixture
def test_data(request):
    data = [{FIELD_NAME: date} for date in request.param]
    return data


@pytest.fixture
def queryset(request):
    data = test_data(request)

    for datum in data:
        DatetimeFilterTestingModel.objects.create(**{
            FIELD_NAME: dateutil.parser.parse(datum[FIELD_NAME])
        })

    return DatetimeFilterTestingModel.objects.all()


FIELD_NAME = 'datetime'


@pytest.mark.django_db
class TestDateRangeFilter(object):

    @date_time_parametrize
    def test_out_of_range(self, dates, test_data, queryset):

        earliest = dates[0]
        beyond_earliest = "1990" + earliest[4:]

        date_filter = DatetimeRangeFilter(FIELD_NAME, {
            "start": beyond_earliest,
            "end": beyond_earliest,
        })
        results_after_filter = date_filter.on_dicts(test_data)
        assert len(results_after_filter) == 0

        results_after_filter = date_filter.on_django_query(queryset)
        assert len(results_after_filter) == 0

        oldest = dates[2]
        beyond_oldest = "2500" + oldest[4:]

        date_filter = DatetimeRangeFilter(FIELD_NAME, {
            "start": beyond_oldest,
            "end": beyond_oldest,
        })
        results_after_filter = date_filter.on_dicts(test_data)
        assert len(results_after_filter) == 0

        results_after_filter = date_filter.on_django_query(queryset)
        assert len(results_after_filter) == 0

    @date_time_parametrize
    def test_date_match_only_one_time_point(self, dates, test_data, queryset):

        date = dates[1]

        date_filter = DatetimeRangeFilter(FIELD_NAME, {
            "start": date,
            "end": date,
        })
        results_after_filter = date_filter.on_dicts(test_data)
        assert len(results_after_filter) == 1

        results_after_filter = date_filter.on_django_query(queryset)
        assert len(results_after_filter) == 1

    @date_time_parametrize
    def test_missing_start_or_end(self, dates, test_data, queryset):

        date = dates[1]

        date_filter = DatetimeRangeFilter(FIELD_NAME, {
            "start": date,
        })

        results_after_filter = date_filter.on_dicts(test_data)
        assert len(results_after_filter) == 2

        results_after_filter = date_filter.on_django_query(queryset)
        assert len(results_after_filter) == 2

        date_filter = DatetimeRangeFilter(FIELD_NAME, {
            "end": date,
        })

        results_after_filter = date_filter.on_dicts(test_data)
        assert len(results_after_filter) == 2

        results_after_filter = date_filter.on_django_query(queryset)
        assert len(results_after_filter) == 2


@pytest.mark.django_db
class TestFilterWithoutTime(object):

    def test_end_date_has_no_time(self):

        datetime_datum = dateutil.parser.parse("2018-12-31T02:00:00+00:00")

        DatetimeFilterTestingModel.objects.create(datetime=datetime_datum)
        test_data = [{
            FIELD_NAME: datetime_datum
        }]

        date_filter = DatetimeRangeFilter(FIELD_NAME, {
            "start": '2018-12-31',
            "end": '2018-12-31',
        })

        result = date_filter.on_dicts(test_data)
        assert len(result) == 1

        queryset = DatetimeFilterTestingModel.objects.all()
        result = date_filter.on_django_query(queryset)
        assert len(result) == 1
