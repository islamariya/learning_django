from django.urls import path

from .views import ContactUs


app_name = 'site_data'

urlpatterns = [
    path('contact/', ContactUs.as_view(), name='contact'),
]