from __future__ import absolute_import

from ..textfilters import TextFullyMatchedFilter


class TestTextFullyMatchedFilter(object):
    def test_text_match(self):
        field_name_to_test = "name"
        text_to_test = "name_example"
        instance_to_test = {
            field_name_to_test: text_to_test
        }
        text_filter = TextFullyMatchedFilter(field_name_to_test, {
            "value": text_to_test
        })
        assert len(text_filter.on_dicts([instance_to_test])) == 1

    def test_text_does_not_match_should_fail(self):
        field_name_to_test = "name"
        text_to_test = "name_example"
        wrong_text_to_test = "not_name_example"
        instance_to_test = {
            field_name_to_test: text_to_test
        }
        text_filter = TextFullyMatchedFilter(field_name_to_test, {
            "value": wrong_text_to_test
        })
        assert len(text_filter.on_dicts([instance_to_test])) == 0
