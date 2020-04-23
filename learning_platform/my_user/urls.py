from django.urls import path, re_path

import my_user.views as my_user
from course.views import StudentsHomeworkListView


app_name = "my_user"

urlpatterns = [
    path("login/", my_user.login, name="login"),
    path("logout/", my_user.logout, name="logout"),
    path("register/", my_user.SignUp.as_view(), name="register"),
    path("profile/", my_user.Profile.as_view(), name="profile"),

    path("profile/my_courses/<int:pk>/", StudentsHomeworkListView.as_view(), name="my_course_homework"),
]