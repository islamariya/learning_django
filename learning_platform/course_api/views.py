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


# Course
class CourseApiViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.filter(is_active=True)
    serializer_class = CourseSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(data='успешно удалено')


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
class CourseLectureSet(viewsets.ModelViewSet):
    queryset = CourseLecture.objects.filter(is_active=True)
    serializer_class = LectureSerilizer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(data='успешно удалено')

    def get_queryset(self):
        '''Gets all lessons registered in Course against a `course`
        query parameter in the URL: api/root/course_lectures?course=2'''
        queryset = CourseLecture.objects.filter(is_active=True)
        course = self.request.query_params.get('course', None)
        if course is not None:
            queryset = queryset.filter(course=course).all()
        return queryset


# Homework
class HomeworkViewSet(viewsets.ModelViewSet):
    queryset = Homework.objects.filter(is_active=True)
    serializer_class = HomeworkSerilizer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(data='успешно удалено')

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
class StudentsEnrolledViewSet(viewsets.ModelViewSet):
    queryset = StudentsEnrolled.objects.filter(is_active=True)
    serializer_class = StudentsenrolledSerilizer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(data='успешно удалено')

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
    queryset = StudentsHomework.objects.filter(status=1)
    serializer_class = StudentsHomeworkCheckingSerilizer


class SendingHomeworkViewSet(viewsets.ModelViewSet):
    queryset = StudentsHomework.objects.all()
    serializer_class = StudentsHomeworkSendSerilizer

    def get_queryset(self):
        user = self.request.user
        queryset = StudentsHomework.objects.filter(student__student__id=user.pk)
        queryset = StudentsHomework.objects.all()
        return queryset

    def perform_update(self, serializer):
        serializer.save(status=1, date_of_completion=datetime.date.today())


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

#
# class CourseApiListView(APIView):
#
#     def get(self, request):
#         items = Course.objects.filter(is_active=True).all()
#         serializer = CourseSerializer(items, many=True)
#         return Response(serializer.data)
#
#     def post(self, request):
#         serializer = CourseSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class CourseApiDetailView(APIView):
#
#     def get(self, request, pk):
#         course = get_object_or_404(Course, pk=pk)
#         serializer = CourseSerializer(course)
#         return Response(serializer.data)
#
#     def put(self, request, pk):
#         course = get_object_or_404(Course, pk=pk)
#         data = request.data
#         serializer = CourseSerializer(course, data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class CourseFlowsApiListView(APIView):
#
#     def get(self, request):
#         items = CourseFlows.objects.filter(is_over=False).all()
#         serializer = CourseFlowsSerializer(items, many=True)
#         return Response(serializer.data)
#
#     def post(self, request):
#         serializer = CourseFlowsSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class CourseFlowsApiDetailView(APIView):
#
#     def get(self, request, pk):
#         course = get_object_or_404(Course, pk=pk)
#         serializer = CourseFlowsSerializer(course)
#         return Response(serializer.data)
#
#     def put(self, request, pk):
#         course = get_object_or_404(Course, pk=pk)
#         data = request.data
#         serializer = CourseFlowsSerializer(course, data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class CourseLectureListView(APIView):
#
#     def get(self, request):
#         items = CourseLecture.objects.filter(is_active=True).all()
#         serializer = LectureSerilizer(items, many=True)
#         return Response(serializer.data)
#
#     def post(self, request):
#         serializer = LectureSerilizer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class LectureApiDetailView(APIView):
#
#     def get(self, request, pk):
#         lecture = get_object_or_404(CourseLecture, pk=pk)
#         serializer = LectureSerilizer(lecture)
#         return Response(serializer.data)
#
#     def put(self, request, pk):
#         lecture = get_object_or_404(CourseLecture, pk=pk)
#         data = request.data
#         serializer = LectureSerilizer(lecture, data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
# #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# class HomeworkListView(APIView):
#
#     def get(self, request):
#         items = Homework.objects.filter(is_active=True).all()
#         serializer = HomeworkSerilizer(items, many=True)
#         return Response(serializer.data)
#
#     def post(self, request):
#         serializer = HomeworkSerilizer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class HomeworkApiDetailView(APIView):
#
#     def get(self, request, pk):
#         homework = get_object_or_404(Homework, pk=pk)
#         serializer = HomeworkSerilizer(homework)
#         return Response(serializer.data)
#
#     def put(self, request, pk):
#         homework = get_object_or_404(Homework, pk=pk)
#         data = request.data
#         serializer = HomeworkSerilizer(homework, data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
# class MyUserListView(APIView):
#
#     def get(self, request):
#         items = MyUser.objects.all()
#         serializer = MyUserSerilizer(items, many=True)
#         return Response(serializer.data)
#
#     def post(self, request):
#         serializer = MyUserSerilizer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
