import graphene

from course.schema import Query as CourseQuery
from course.schema import Mutation as CourseMutation


class Query(CourseQuery, graphene.ObjectType):
    pass


class Mutation(CourseMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)