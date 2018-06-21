from __future__ import absolute_import

import datetime

from dateutil import parser
import pytz

from .base import FieldFilter, DictFilterMixin, DjangoQueryFilterMixin
from .queryfilter import QueryFilter


WHOLE_DAY = datetime.timedelta(days=1)
ONE_SECOND = datetime.timedelta(seconds=1)


@QueryFilter.register_type_condition('datetime')
class DatetimeRangeFilter(DjangoQueryFilterMixin, DictFilterMixin,
                          FieldFilter):

    @property
    def start(self):
        return get_start(self.filter_args.get("start"))

    @property
    def end(self):
        end_datetime = get_end(self.filter_args.get("end"))

        if not end_datetime:
            return None

        if _has_no_time_info(end_datetime):
            end_datetime = end_datetime + WHOLE_DAY - ONE_SECOND

        return end_datetime

    def on_dicts(self, dicts):

        def in_range(datum):
            datetime_string = self.get(datum, self.field_name)
            if isinstance(datetime_string, datetime.datetime):
                to_compare = datetime_string
            else:
                to_compare = parse(datetime_string)

            if self.start and (to_compare < self.start):
                return False

            if self.end and (self.end < to_compare):
                return False

            return True

        return list(filter(in_range, dicts))

    def _do_django_query(self, queryset):
        query_dict = dict()

        if self.start:
            query_dict["{}__gte".format(self.field_name)] = self.start

        if self.end:
            query_dict["{}__lte".format(self.field_name)] = self.end

        if query_dict:
            return queryset.filter(**query_dict)
        else:
            return queryset


min_datetime = datetime.datetime.min.replace(tzinfo=pytz.utc)
max_datetime = datetime.datetime.max.replace(tzinfo=pytz.utc)


def get_start(start_date_str):
    if not start_date_str:
        return None
    return parse(start_date_str)


def get_end(end_date_str):
    if not end_date_str:
        return None
    return parse(end_date_str)


def parse(datetime_string):
    return make_time_aware(parser.parse(datetime_string))


def make_time_aware(datetime_data):

    if not datetime_data.tzinfo:
        datetime_data = datetime_data.replace(tzinfo=pytz.utc)
    return datetime_data


def _has_no_time_info(value):
    return value.hour == 0 and \
           value.minute == 0 and \
           value.second == 0 and \
           value.microsecond == 0
