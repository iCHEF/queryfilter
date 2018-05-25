from __future__ import absolute_import

from graphene.test import Client

from examples.schema import EXAMPLE_DATA, example_schema


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

    def test_number_graphql(self):
        client = Client(example_schema)
        target_data_price = EXAMPLE_DATA[0].get("price")
        query = '''
            {
                something(queryFilter: {
                    price: {
                        min: %s
                        max: %s
                    }
                }){
                    price
                }
            }
        ''' % (target_data_price-1, target_data_price+1)
        executed = client.execute(query)
        data = executed["data"]
        assert len(data["something"]) == 1
        query_result = data["something"][0]
        assert query_result.get("price") == target_data_price

    def test_number_select_graphql(self):
        client = Client(example_schema)
        target_data_type = EXAMPLE_DATA[0].get("type")
        query = '''
            {
                something(queryFilter: {
                    type: {
                        values: [%s]
                    }
                }){
                    type
                }
            }
        ''' % target_data_type
        executed = client.execute(query)
        data = executed["data"]
        assert len(data["something"]) == 1
        query_result = data["something"][0]
        assert query_result.get("type") == target_data_type

    def test_text_select_graphql(self):
        client = Client(example_schema)
        target_data_category = EXAMPLE_DATA[0].get("category")
        query = '''
            {
                something(queryFilter: {
                    category: {
                        values: ["%s"]
                    }
                }){
                    category
                }
            }
        ''' % target_data_category
        executed = client.execute(query)
        data = executed["data"]
        assert len(data["something"]) == 1
        query_result = data["something"][0]
        assert query_result.get("category") == target_data_category

    def test_birthday_graphql(self):
        client = Client(example_schema)
        query = '''
            {
                something(queryFilter: {
                    birthday: {
                        start: "04/01"
                        end: "06/01"
                    }
                }){
                    birthday
                }
            }
        '''
        executed = client.execute(query)
        data = executed["data"]
        assert len(data["something"]) == 1
        query_result = data["something"][0]
        assert query_result.get("birthday") == "05/20"

    def test_datetime_graphql(self):
        client = Client(example_schema)
        query = '''
            {
                something(queryFilter: {
                    datetime: {
                        start: "2018-05-25"
                        end: "2018-05-25"
                    }
                }){
                    datetime
                }
            }
        '''
        executed = client.execute(query)
        data = executed["data"]
        assert len(data["something"]) == 1
        query_result = data["something"][0]
        assert query_result.get("datetime") == "2018-05-25"
