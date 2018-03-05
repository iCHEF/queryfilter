from __future__ import absolute_import

from .base import FieldFilter
from .queryfilter import QueryFilter


@QueryFilter.register_type_condition('birthday', 'age_range')
class BirthdayAgeRangeFilter(FieldFilter):
    def on_dicts(self, dicts):
        range_start = self.filter_args.get("start")
        if range_start is not None:
            range_start_int = int(range_start)
        range_end = self.filter_args.get("end")
        if range_end is not None:
            range_end_int = int(range_end)

        def by_value_of_dict_field_in_range(dictobj):
            birth_year = dictobj.get(self.field_name)
            age = self.count_age(birth_year)
            return (
                (range_start is None or age >= range_start_int)
                and
                (range_end is None or age <= range_end_int)
            )

        return list(filter(by_value_of_dict_field_in_range, dicts))


@QueryFilter.register_type_condition('birthday', 'date_range')
class BirthdayDateRangeFilter(FieldFilter):
    def split_month_day(self, birth):
        month, day = birth.split("/")
        return int(month), int(day)

    def on_dicts(self, dicts):
        range_start = self.filter_args.get("start")
        range_end = self.filter_args.get("end")
        to_filter_with_range_start = range_start is not None
        to_filter_with_range_end = range_end is not None
        if not to_filter_with_range_start and not to_filter_with_range_end:
            return dicts

        if to_filter_with_range_start:
            month_start, day_start = self.split_month_day(range_start)
        if to_filter_with_range_end:
            month_end, day_end = self.split_month_day(range_end)

        def in_date_range_across_year_end(month, day):
            if (month > month_start):
                return True
            if (month == month_start) and day >= day_start:
                return True
            if (month < month_end):
                return True
            if (month == month_end) and day <= day_start:
                return True
            return False

        def larger_or_equal_to_range_start(month, day):
            if month < month_start:
                return False
            if month == month_start and day < day_start:
                return False
            return True

        def smaller_or_equal_to_range_end(month, day):
            import alog
            alog.info((month, day))
            alog.info((month_end, day_end))
            if month < month_end:
                alog.info("V")
                return True
            if month == month_end and day <= day_end:
                alog.info("V")
                return True
            alog.info("V")
            return False

        def filter_both_start_and_end(month, day):
            range_across_year_end = month_end < month_start
            if range_across_year_end:
                return in_date_range_across_year_end(month, day)
            return (larger_or_equal_to_range_start(month, day)
                    and smaller_or_equal_to_range_end(month, day))

        def in_given_range(month, day):
            if to_filter_with_range_start and to_filter_with_range_end:
                return filter_both_start_and_end(month, day)

            if to_filter_with_range_start:
                return larger_or_equal_to_range_start(month, day)

            if to_filter_with_range_end:
                return smaller_or_equal_to_range_end(month, day)

        def by_value_of_dict_field_in_range(dictobj):
            value = dictobj.get(self.field_name)
            month, day = self.split_month_day(value)
            return in_given_range(month, day)

        return list(filter(by_value_of_dict_field_in_range, dicts))
