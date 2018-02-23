from __future__ import absolute_import

from ..queryfilter import QueryFilter


class TestTextFilter(object):
    def setup(self):
        self.field_name_to_test = "name"
        self.text_to_test = "name_example"
        self.dicts = [
            {self.field_name_to_test: self.text_to_test}
        ]

    def test_query_filter(self):
        query_filter = QueryFilter({
            "name": {
                "type": "string",
                "condition": "contains",
                "value": self.field_name_to_test
            }
        })

        assert len(query_filter.on_dicts(self.dicts)) == 1
