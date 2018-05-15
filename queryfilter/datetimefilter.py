from __future__ import absolute_import

import datetime

from dateutil import parser
import pytz

from .base import FieldFilter, DictFilterMixin, DjangoQueryFilterMixin
from .queryfilter import QueryFilter


@QueryFilter.register_type_condition('datetime', 'datetime_range')
class DatetimeRangeFilter(DjangoQueryFilterMixin, DictFilterMixin, FieldFilter):

    @property
    def start(self):
        return get_start(self.filter_args.get("start"))

    @property
    def end(self):
        return get_end(self.filter_args.get("end"))

    def on_dicts(self, dicts):

        def in_range(datum):
            datetime_string = self.get(datum, self.field_name)
            if isinstance(datetime_string, datetime.datetime):
                to_compare = datetime_string
            else:
                to_compare = parse(datetime_string)
            return self.start <= to_compare <= self.end

        return list(filter(in_range, dicts))

    def do_filter(self, queryset):
        query_dict = {
            "{}__gte".format(self.field_name): self.start,
            "{}__lte".format(self.field_name): self.end,
        }
        return queryset.filter(**query_dict)


min_datetime = datetime.datetime.min.replace(tzinfo=pytz.utc)
max_datetime = datetime.datetime.max.replace(tzinfo=pytz.utc)


def get_start(start_date_str):
    if not start_date_str:
        return min_datetime
    return parse(start_date_str)


def get_end(end_date_str):
    if not end_date_str:
        return max_datetime
    return parse(end_date_str)


def parse(datetime_string):
    return parser.parse(datetime_string)
