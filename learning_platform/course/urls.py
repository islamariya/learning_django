from django.urls import path, include

import course.views as course

app_name = 'course'

urlpatterns = [
    path("", course.CoursesFlowsListView.as_view(), name="index"),
    path("all_courses/", course.CoursesListView.as_view(), name="all_courses"),
    path("all_courses/<int:pk>/", course.CourseDetailView.as_view(), name="course_detail"),

    path("courses/<int:pk>/", course.CourseFlowsDetailView.as_view(), name="course_flow_detail"),
    path("courses/create/", course.CourseCreateView.as_view(), name="course_create"),
    path("courses/<int:pk>/update/", course.CourseUpdateView.as_view(), name="course_update"),
    path("courses/<int:pk>/delete", course.CourseDeleteView.as_view(), name="course_delete"),

    path("flows/", course.CoursesFlowsListView.as_view(), name="all_flows"),
    path("flows/create/", course.CourseFlowsCreateView.as_view(), name="create_flow"),
    path("flows/<int:pk>/update", course.CourseFlowsUpdateView.as_view(), name="flow_update"),
    path("flows/<int:pk>/delete", course.CourseFlowsDeleteView.as_view(), name="flow_delete"),

    path("courses/<int:pk>/lectures/", course.LectureListView.as_view(), name="lectures"),
    path("lectures/<int:pk>", course.LectureDetailView.as_view(),
         name="lectures_detail"),
    path("lectures/<int:pk>/update/", course.LectureUpdateView.as_view(), name="lecture_update"),
    path("lectures/<int:pk>/delete", course.LectureDeleteView.as_view(), name="lecture_delete"),

    path("courses/<int:pk>/timetable/", course.FlowTimetableListView.as_view(), name="timetable"),
    path("timetable/<int:pk>/", course.LectureTimetableDetailView.as_view(), name="timetable_detail"),
    path("timetable/<int:pk>/update/", course.LectureTimetableUpdateView.as_view(),
         name="timetable_update"),
    path("timetable/<int:pk>/delete/", course.LectureTimetableDeleteView.as_view(),
         name="timetable_delete"),

    path("courses/<int:pk>/homework/", course.HomeworkListView.as_view(), name="homework"),
    path("homework/<int:pk>/", course.HomeworkDetailView.as_view(), name="homework_detail"),
    path("homework/<int:pk>/update/", course.HomeworkUpdateView.as_view(), name="homework_update"),
    path("homework/<int:pk>/delete/", course.HomeworkDeleteView.as_view(), name="homework_delete"),

    path("my_homework/<int:pk>/", course.StudentHomeworkDetailView.as_view(), name="my_homework_detail"),
    path("my_homework/<int:pk>/update/", course.StudentHomeworkSendView.as_view(), name="send_homework"),
    path("homework_for_review/<int:pk>/", course.StudentsHomeworkListView.as_view(), name="homework_review"),
]