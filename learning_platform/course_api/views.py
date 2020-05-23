import datetime

from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import status, viewsets
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


# CourseFlow
class CourseFlowsViewSet(viewsets.ModelViewSet):
    queryset = CourseFlows.objects.filter(is_over=False)
    serializer_class = CourseFlowsSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_over = True
        instance.save()
        return Response(data='успешно удалено')


# CourseLecture
class CourseLectureSet(DestroyMixin,viewsets.ModelViewSet):
    serializer_class = LectureSerilizer

    def get_queryset(self):
        '''Gets all lessons registered in Course against a `course`
        query parameter in the URL: api/root/course_lectures?course=2'''
        queryset = CourseLecture.objects.filter(is_active=True)
        course = self.request.query_params.get('course', None)
        if course is not None:
            queryset = queryset.filter(course=course)
        return queryset


# Homework
class HomeworkViewSet(DestroyMixin, viewsets.ModelViewSet):
    queryset = Homework.objects.filter(is_active=True)
    serializer_class = HomeworkSerilizer

    def get_queryset(self):
        '''Gets all homework needed to be done in CourseFlow against a `course_flow`
        query parameter in the URL: api/root/homework?course_flow=2'''
        queryset = Homework.objects.filter(is_active=True)
        course_flow = self.request.query_params.get('course_flow', None)
        if course_flow is not None:
            queryset = queryset.filter(course_flow=course_flow)
        return queryset


# User
class MyUserViewSet(viewsets.ModelViewSet):
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerilizer


# StudentsEnrolled
class StudentsEnrolledViewSet(DestroyMixin, viewsets.ModelViewSet):
    queryset = StudentsEnrolled.objects.filter(is_active=True)
    serializer_class = StudentsenrolledSerilizer

    @action(methods=['get'], detail=True)
    def my_courses(self, request, pk=None):
        """Returns all courses_flows current user enrolled. """
        user = request.user
        courses = StudentsEnrolled.objects.filter(student=user)
        serializer = StudentsenrolledSerilizer(courses, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        '''Gets all students registered in CourseFlow against a `course_flow`
        query parameter in the URL: api/root/studentsEnrolled?course_flow=2'''
        queryset = StudentsEnrolled.objects.filter(is_active=True)
        course_flow = self.request.query_params.get('course_flow', None)
        if course_flow is not None:
            queryset = queryset.filter(course_flow=course_flow)
        return queryset


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


class SendingHomeworkViewSet(viewsets.ModelViewSet):
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

    def get_queryset(self):
        course_flow = self.request.query_params.get('course_flow', None)
        queryset = CourseFlowTimetable.objects.filter
        if course_flow is not None:
            queryset = queryset.filter(course_flow=course_flow)
        return queryset
