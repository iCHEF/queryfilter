from __future__ import absolute_import

from ..textfilters import (
    TextFullyMatchedFilter, TextPartialMatchedFilter,
    TextStartsWithMatchedFilter, TextEndsWithMatchedFilter
)


class TestTextFilterMixin(object):
    def setup(self):
        self.field_name_to_test = "name"
        self.text_to_test = "name_example"
        self.dicts = [
            {self.field_name_to_test: self.text_to_test}
        ]


class TestTextFullyMatchedFilter(TestTextFilterMixin):
    def test_text_fully_match(self):
        text_filter = TextFullyMatchedFilter(self.field_name_to_test, {
            "value": self.text_to_test
        })
        assert len(text_filter.on_dicts(self.dicts)) == 1

    def test_text_does_not_fully_match_should_fail(self):
        text_not_match = "not_name_example"
        text_filter = TextFullyMatchedFilter(self.field_name_to_test, {
            "value": text_not_match
        })
        assert len(text_filter.on_dicts(self.dicts)) == 0


class TestTextPartialMatchedFilter(TestTextFilterMixin):
    def test_text_partial_match(self):
        text_filter = TextPartialMatchedFilter(self.field_name_to_test, {
            "value": self.text_to_test[:1]
        })
        assert len(text_filter.on_dicts(self.dicts)) == 1

    def test_text_does_not_partial_match_should_fail(self):
        text_not_match = "not"
        text_filter = TextPartialMatchedFilter(self.field_name_to_test, {
            "value": text_not_match
        })
        assert len(text_filter.on_dicts(self.dicts)) == 0


class TestTextStartsWithMatchedFilter(TestTextFilterMixin):
    def test_text_partial_match(self):
        text_filter = TextStartsWithMatchedFilter(self.field_name_to_test, {
            "value": self.text_to_test[:1]
        })
        assert len(text_filter.on_dicts(self.dicts)) == 1

    def test_text_does_not_partial_match_should_fail(self):
        text_not_match = "not"
        text_filter = TextStartsWithMatchedFilter(self.field_name_to_test, {
            "value": text_not_match
        })
        assert len(text_filter.on_dicts(self.dicts)) == 0

        text_not_match_with_endwith = self.text_to_test[-1:]
        text_filter = TextStartsWithMatchedFilter(self.field_name_to_test, {
            "value": text_not_match_with_endwith
        })
        assert len(text_filter.on_dicts(self.dicts)) == 0


class TestTextEndsWithMatchedFilter(TestTextFilterMixin):
    def test_text_partial_match(self):
        text_filter = TextEndsWithMatchedFilter(self.field_name_to_test, {
            "value": self.text_to_test[-1:]
        })
        assert len(text_filter.on_dicts(self.dicts)) == 1

    def test_text_does_not_partial_match_should_fail(self):
        text_not_match = "not"
        text_filter = TextEndsWithMatchedFilter(self.field_name_to_test, {
            "value": text_not_match
        })
        assert len(text_filter.on_dicts(self.dicts)) == 0

        text_not_match_with_startwith = self.text_to_test[:1]
        text_filter = TextEndsWithMatchedFilter(self.field_name_to_test, {
            "value": text_not_match_with_startwith
        })
        assert len(text_filter.on_dicts(self.dicts)) == 0
