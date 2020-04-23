from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core import validators
from django.utils.translation import ugettext_lazy as _


class PhoneValidator(validators.RegexValidator):
    """Checks if phone_number consists of 10 digits and starts with 9 in format 9xxxxxxxxx"""
    regex = r'^9\d{9}$'
    message = "Enter a valid mobile phone number without country code or +. Phone number must contain 10 digits and " \
              "be entered in the format 9xxxxxxxxx"

    flags = 0


class MyUserManager(BaseUserManager):
    """Define a model manager for User without username"""
    use_in_migrations = True

    def _create_user(self, phone_number, password, **extra_fields):
        if not phone_number:
            raise ValueError("Phone number is required")
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(phone_number, password, **extra_fields)

    def create_superuser(self, phone_number, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self._create_user(phone_number, password, **extra_fields)



class MyUser(AbstractUser):
    """This class represents Users, authentication via phone_number. Is_student is a flag shown if User is student
    at any Course. is_stuff = True provide access to admin panel. """
    phone_validator = PhoneValidator()
    phone_number = models.CharField(max_length=10,
                                    unique=True,
                                    verbose_name="Номер телефона",
                                    help_text="Field required. Enter a valid number without country code or +",
                                    validators=[phone_validator],
                                    error_messages={"unique": "A user with this phone number already exists"},
                                    )

    username = None
    is_teacher = models.BooleanField(default=False, verbose_name='Является ли преподавателем')
    is_student = models.BooleanField(default=False, verbose_name='Является ли студентом')
    date_of_birth = models.DateField(verbose_name='Дата рождения', blank=True, null=True)
    email = models.EmailField(verbose_name='Email')

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []
    objects = MyUserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        self.full_name = self.get_full_name()
        return self.full_name
