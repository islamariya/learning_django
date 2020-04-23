from django.test import TestCase
from django.contrib.auth import get_user_model


class UserManagerTest(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user()
