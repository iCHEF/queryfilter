from __future__ import absolute_import

from ..textfilters import TextFullyMatchedFilter


class TestTextFullyMatchedFilter(object):
    def setup(self):
        self.field_name_to_test = "name"
        self.text_to_test = "name_example"
        self.dicts = [
            {self.field_name_to_test: self.text_to_test}
        ]

    def test_text_match(self):
        text_filter = TextFullyMatchedFilter(self.field_name_to_test, {
            "value": self.text_to_test
        })
        assert len(text_filter.on_dicts(self.dicts)) == 1

    def test_text_does_not_match_should_fail(self):
        text_not_match = "not_name_example"
        text_filter = TextFullyMatchedFilter(self.field_name_to_test, {
            "value": text_not_match
        })
        assert len(text_filter.on_dicts(self.dicts)) == 0
