import datetime

from django_filters import rest_framework as filters
from rest_framework.response import Response
from rest_framework import filters, viewsets
from rest_framework.decorators import action

from course.models import Course, CourseFlows, Homework, CourseLecture, \
    StudentsEnrolled, StudentsHomework, CourseFlowTimetable

from my_user.models import MyUser

from .serializers import CourseSerializer, CourseFlowsSerializer, HomeworkSerilizer, \
    LectureSerilizer, MyUserSerilizer, StudentsenrolledSerilizer, StudentsHomeworkSerilizer, \
    CourseFlowTimetableSerilizer, StudentsHomeworkCheckingSerilizer, StudentsHomeworkSendSerilizer


class DestroyMixin(object):
    """Provides soft delete by changing flag is_active = False """

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(data='успешно удалено')


# Course
class CourseApiViewSet(DestroyMixin, viewsets.ModelViewSet):

    queryset = Course.objects.filter(is_active=True)
    serializer_class = CourseSerializer
    filterset_fields = ["category"]


# CourseFlow
class CourseFlowsViewSet(DestroyMixin, viewsets.ModelViewSet):

    queryset = CourseFlows.objects.filter(is_active=True)
    serializer_class = CourseFlowsSerializer
    filterset_fields = ["course", "course__category"]


# CourseLecture
class CourseLectureSet(DestroyMixin,viewsets.ModelViewSet):

    queryset = CourseLecture.objects.filter(is_active=True)
    serializer_class = LectureSerilizer
    filterset_fields = ["course", "sequence_number"]


# Homework
class HomeworkViewSet(DestroyMixin, viewsets.ModelViewSet):

    queryset = Homework.objects.filter(is_active=True)
    serializer_class = HomeworkSerilizer
    filterset_fields = ["course_flow", "sequence_number"]


# User
class MyUserViewSet(viewsets.ModelViewSet):

    queryset = MyUser.objects.all()
    serializer_class = MyUserSerilizer
    filterset_fields = ["is_teacher", "is_student"]


# StudentsEnrolled
class StudentsEnrolledViewSet(DestroyMixin, viewsets.ModelViewSet):

    queryset = StudentsEnrolled.objects.filter(is_active=True)
    serializer_class = StudentsenrolledSerilizer
    filterset_fields = ["course_flow"]

    @action(methods=['get'], detail=True)
    def my_courses(self, request):
        """Returns all courses_flows current user enrolled. """
        user = request.user
        courses = StudentsEnrolled.objects.filter(student=user)
        serializer = StudentsenrolledSerilizer(courses, many=True)
        return Response(serializer.data)


# StudentsHomework
class StudentsHomeworkViewSet(viewsets.ModelViewSet):

    queryset = StudentsHomework.objects.all()
    serializer_class = StudentsHomeworkSerilizer

    def get_queryset(self):
        user = self.request.user
        course_flow = self.request.query_params.get('course_flow', None)
        queryset = StudentsHomework.objects.filter(student__student__id=user.pk)
        if course_flow is not None:
            queryset = queryset.filter(course_flow=course_flow)
        return queryset


class CheckingHomeworkViewSet(viewsets.ModelViewSet):

    queryset = StudentsHomework.objects.filter(status=StudentsHomework.HOMEWORK_STATUS_ON_REVIEW)
    serializer_class = StudentsHomeworkCheckingSerilizer
    filterset_fields = ["course_flow"]


class SendingHomeworkViewSet(viewsets.ModelViewSet):
    """Provides list of homework made by current user. User fills in field "content".
    Update method changes status to ON_REVIEW and update date_of_completion to current date"""

    queryset = StudentsHomework.objects.all()
    serializer_class = StudentsHomeworkSendSerilizer

    def get_queryset(self):
        user = self.request.user
        queryset = StudentsHomework.objects.filter(student__student__id=user.pk)
        return queryset

    def perform_update(self, serializer):
        serializer.save(status=StudentsHomework.HOMEWORK_STATUS_ON_REVIEW, date_of_completion=datetime.date.today())


# CourseFlowTimetable
class CourseFlowTimetableViewSet(viewsets.ModelViewSet):

    queryset = CourseFlowTimetable.objects.all()
    serializer_class = CourseFlowTimetableSerilizer
    filterset_fields = ["course_flow", "lesson__sequence_number"]
