import graphene

from graphene_django.types import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from .models import (CourseCategory,
                     Course,
                     CourseLecture,
                     CourseFlows,
                     Homework,
                     StudentsEnrolled,
                     StudentsHomework,
                     CourseFlowTimetable)
from my_user.models import MyUser


class MyUserType(DjangoObjectType):
    class Meta:
        model = MyUser


class CourseCategoryType(DjangoObjectType):
    class Meta:
        model = CourseCategory


class CourseType(DjangoObjectType):
    class Meta:
        model = Course


class CourseLectureType(DjangoObjectType):
    class Meta:
        model = CourseLecture


class CourseFlowType(DjangoObjectType):
    class Meta:
        model = CourseFlows
        filter_fields = ("course", )
        # filter_fields = {
        #     'course': ['exact',],
        #     'start_date': ['lte', 'gte']
        # }
        interfaces = (graphene.relay.Node,)


class HomeworkType(DjangoObjectType):
    class Meta:
        model = Homework


class StudentEnrolleType(DjangoObjectType):
    class Meta:
        model = StudentsEnrolled


class StudentsHomeworkType(DjangoObjectType):
    class Meta:
        model = StudentsHomework


class CourseFlowTimetable(DjangoObjectType):
    class Meta:
        model = CourseFlowTimetable


class Query:
    all_courses = graphene.List(CourseType)
    retrieve_course = graphene.Field(CourseType, id=graphene.Int(), name=graphene.String())

    all_lessons_in_course = graphene.List(CourseLectureType, id=graphene.Int(), course=graphene.Int())
    retrieve_lesson = graphene.Field(CourseLectureType, id=graphene.Int())

    all_course_flows = graphene.List(CourseFlowType, id=graphene.Int())
    retrieve_course_flow = graphene.Field(CourseFlowType, id=graphene.Int())
    filtered_course_flows = DjangoFilterConnectionField(CourseFlowType)

    def resolve_retrieve_course(self, info, *args, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            return Course.objects.get(pk=id)
        return None

    def resolve_all_courses(self, info, *args, **kwargs):
        return Course.objects.filter(is_active=True).all()

    def resolve_retrieve_lesson(self, info, id):
        return CourseLecture.objects.get(pk=id)

    def resolve_all_lessons_in_course(self, info, course, *args, **kwargs):
        return CourseLecture.objects.filter(is_active=True, course=course).all()

    def resolve_all_course_flows(self, info, *args, **kwargs):
        return CourseFlows.objects.filter(is_over=False).all()

    def resolse_retrieve_course_flow(self, info, *args, **kwargs):
        if 'course_flow' in kwargs:
            return CourseFlows.objects.get(pk=id)
        return None

    # if info.context.user.is_student:
    #     return Course.objects.filter(is_active=True).all()
    # else:
    #     return Course.objects.none()
