import json

from graphene_django.utils.testing import GraphQLTestCase
from django.test import TestCase

from learning_platform.schema import schema


class GQLTestCase(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema

    def test_some_query(self):
        response = self.query(
            '''
            query {
              allSchools{
                id
                name
              }
            }
            ''',
            op_name='allSchools'
        )

        content = json.loads(response.content)
        self.assertResponseNoErrors(response)