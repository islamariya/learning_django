import graphene

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.shortcuts import get_object_or_404
from graphene_django.types import DjangoObjectType

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


class HomeworkType(DjangoObjectType):
    class Meta:
        model = Homework


class StudentEnrolleType(DjangoObjectType):
    class Meta:
        model = StudentsEnrolled


class StudentsHomeworkType(DjangoObjectType):
    class Meta:
        model = StudentsHomework


class CourseFlowTimetableType(DjangoObjectType):
    class Meta:
        model = CourseFlowTimetable


class CourseCategoryMutation(graphene.Mutation):

    class Arguments:
        category_id = graphene.Int(required=True)
        title = graphene.String(required=True)
        is_active = graphene.Boolean()

    result = graphene.Boolean()
    course_category = graphene.Field(CourseCategoryType)

    def mutate(self, info, category_id, title, is_active):
        result = False
        try:
            category_instance = CourseCategory.objects.get(pk=category_id)
        except (ObjectDoesNotExist, MultipleObjectsReturned):
            category_instance = None
            print("Объект не найден или их больше 1")

        if category_instance is not None:
            category_instance.title = title
            category_instance.is_active = is_active
            category_instance.save()
            result = True
            return CourseCategoryMutation(result=result, course_category=category_instance)
        return CourseCategoryMutation(result=result, course_category = None)


class Mutation:
    update_category = CourseCategoryMutation.Field()


class Query:
    all_courses = graphene.List(CourseType)
    retrieve_course = graphene.Field(CourseType, id=graphene.Int())

    all_lessons_in_course = graphene.List(CourseLectureType, course=graphene.Int())
    # all types of lessons should be taught in course_flow
    retrieve_lesson = graphene.Field(CourseLectureType, id=graphene.Int())

    all_course_flows = graphene.List(CourseFlowType)
    retrieve_course_flow = graphene.Field(CourseFlowType, id=graphene.Int())

    all_course_homework = graphene.List(HomeworkType, course_flow=graphene.Int())
    retrieve_course_homework = graphene.Field(HomeworkType, id=graphene.Int())

    course_timetable = graphene.List(CourseFlowTimetableType, course_flow=graphene.Int())
    # exact lesson in course_flow on specific date
    retrieve_course_flow_lesson = graphene.Field(CourseFlowTimetableType, id=graphene.Int())

    all_students_enrolled = graphene.List(StudentEnrolleType, course_flow=graphene.Int())

    # all particular student's homework in particular course_flow
    all_students_homework = graphene.List(StudentsHomeworkType, student=graphene.Int(),
                                           course_flow=graphene.Int())

    retrieve_student_homework = graphene.Field(StudentsHomeworkType, id=graphene.Int())

    def resolve_retrieve_course(self, info, id):
        return get_object_or_404(Course, pk=id)

    def resolve_all_courses(self, info, *args, **kwargs):
        return Course.objects.filter(is_active=True)

    def resolve_retrieve_lesson(self, info, id):
        return get_object_or_404(CourseLecture, pk=id)

    def resolve_all_lessons_in_course(self, info, course, *args, **kwargs):
        return CourseLecture.objects.filter(is_active=True, course=course)

    def resolve_all_course_flows(self, info, *args, **kwargs):
        return CourseFlows.objects.filter(is_over=False)

    def resolve_retrieve_course_flow(self, info, id):
        return get_object_or_404(CourseFlows, pk=id)

    def resolve_all_course_homework(self, info, course_flow, *args, **kwargs):
        return Homework.objects.filter(course_flow=course_flow)

    def resolve_retrieve_course_homework(self, info, id):
        return get_object_or_404(Homework, pk=id)

    def resolve_course_timetable(self, info, course_flow):
        return CourseFlowTimetable.objects.filter(course_flow=course_flow)

    def resolve_retrieve_course_flow_lesson(self, info, id):
        return get_object_or_404(CourseFlowTimetable, pk=id)

    def resolve_all_students_enrolled(self, info, course_flow):
        return StudentsEnrolled.objects.filter(course_flow=course_flow)

    def resolve_all_students_homework(self, info, course_flow, student):
        return StudentsHomework.objects.filter(course_flow=course_flow, student__student__id=student)

    def resolve_retrieve_student_homework(self, info, id):
        return get_object_or_404(StudentsHomework, pk=id)
