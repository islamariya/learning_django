from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views as jwt_views

from .views import CourseApiViewSet, CourseFlowsViewSet, HomeworkViewSet, \
    CourseLectureSet, MyUserViewSet, StudentsEnrolledViewSet, StudentsHomeworkViewSet, \
    CourseFlowTimetableViewSet, CheckingHomeworkViewSet, SendingHomeworkViewSet


app_name = "course_api"

router = DefaultRouter()
router.register("course", CourseApiViewSet)
router.register("course_flows", CourseFlowsViewSet)
router.register("course_lectures", CourseLectureSet, basename="CourseLecture")
router.register("homework", HomeworkViewSet)
router.register("users", MyUserViewSet)
router.register("students_enrolled", StudentsEnrolledViewSet)
router.register("students_homework", StudentsHomeworkViewSet)
router.register("course_timetable", CourseFlowTimetableViewSet)
router.register("checking_homework", CheckingHomeworkViewSet)
router.register("send_homework", SendingHomeworkViewSet)

urlpatterns = [
    path("token/", jwt_views.TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"),
    path("root/", include(router.urls)),
    path("students_enrolled/my_courses",
         StudentsEnrolledViewSet.as_view({'get':'my_courses'})),
]