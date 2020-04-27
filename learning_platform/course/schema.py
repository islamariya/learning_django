import graphene

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


class CourseFlowTimetable(DjangoObjectType):
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
        category_instance = CourseCategory.objects.get(pk=category_id)
        if category_instance:
            category_instance.title = title
            category_instance.is_active = is_active
            category_instance.save()
            result = True
            return CourseCategoryMutation(result=result, course_category = category_instance)
        return CourseCategoryMutation(result=result, course_category = None)


class Mutation:
    update_category = CourseCategoryMutation.Field()


class Query:
    all_courses = graphene.List(CourseType)
    retrieve_course = graphene.Field(CourseType, id=graphene.Int(), name=graphene.String())

    all_lessons_in_course = graphene.List(CourseLectureType, id=graphene.Int(), course=graphene.Int())
    # all types of lessons should be taught in course_flow
    retrieve_lesson = graphene.Field(CourseLectureType, id=graphene.Int())

    all_course_flows = graphene.List(CourseFlowType, id=graphene.Int())
    retrieve_course_flow = graphene.Field(CourseFlowType, id=graphene.Int())

    all_course_homework = graphene.List(HomeworkType, course_flow=graphene.Int())
    retrieve_course_homework = graphene.Field(HomeworkType, id=graphene.Int())

    course_timetable = graphene.List(CourseFlowTimetable, course_flow=graphene.Int())
    # exact lesson in course_flow on specific date
    retrieve_course_flow_lesson = graphene.Field(CourseFlowTimetable, id=graphene.Int())

    all_students_enrolled = graphene.List(StudentEnrolleType, course_flow=graphene.Int())

    # all particular student's homework in particular course_flow
    all_students_homework = graphene.List(StudentsHomeworkType, student=graphene.Int(),
                                           course_flow=graphene.Int())

    retrieve_student_homework = graphene.Field(StudentsHomeworkType, id=graphene.Int())

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

    def resolve_retrieve_course_flow(self, info, id):
        return CourseFlows.objects.get(pk=id)

    def resolve_all_course_homework(self, info, course_flow, *args, **kwargs):
        return Homework.objects.filter(course_flow=course_flow).all()

    def resolve_retrieve_course_homework(self, info, id):
        return Homework.objects.get(pk=id)

    def resolve_course_timetable(self, info, course_flow):
        return CourseFlowTimetable.objects.filter(course_flow=course_flow).all()

    def resolve_course_flow_lesson(self, info, id):
        return CourseFlowTimetable.get(pk=id)

    def resolve_all_students_enrolled(self, info, course_flow):
        return StudentsEnrolled.objects.filter(course_flow=course_flow).all()

    def resolve_all_students_homework(self, info, course_flow, student):
        return StudentsHomework.objects.filter(course_flow=course_flow, student__student__id=student).all()

    def resolve_retrieve_student_homework(self, info, id):
        return StudentsHomework.objects.get(pk=id)


    # if info.context.user.is_student:
    #     return Course.objects.filter(is_active=True).all()
    # else:
    #     return Course.objects.none()
