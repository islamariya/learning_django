"""learning_platform URL Configuration"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings

from graphene_django.views import GraphQLView
from .schema import schema


urlpatterns = [
    path('', include('course.urls', namespace='courses')),
    path('admin/', admin.site.urls),
    path('users/', include('my_user.urls', namespace='users')),
    path('about/', include('site_data.urls', namespace="about")),
    path('api/', include('course_api.urls', namespace='course_api')),
    path('graphql/', GraphQLView.as_view(graphiql=True, schema=schema)),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns.append(
        path('__debug__/', include(debug_toolbar.urls)),
                       )