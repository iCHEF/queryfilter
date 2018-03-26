from __future__ import absolute_import

from graphene.test import Client

from queryfilter.examples.schema import EXAMPLE_DATA, example_schema


class TestGraphQLSchema(object):
    def test_text_graphql(self):
        client = Client(example_schema)
        target_data_name = EXAMPLE_DATA[0].get("name")
        query = '''
            {
                something(queryFilter: {
                    name: {
                        value: "%s"
                    }
                }){
                    name
                }
            }
        ''' % target_data_name
        executed = client.execute(query)
        data = executed["data"]
        assert len(data["something"]) == 1
        query_result = data["something"][0]
        assert query_result.get("name") == target_data_name
