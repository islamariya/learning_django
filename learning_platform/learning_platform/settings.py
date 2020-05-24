import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open('learning_platform/private_data/secret_keys.txt') as s_key:
    SECRET_KEY = s_key.read().strip()

DEBUG = True

with open('learning_platform/private_data/admin_data.txt') as admin_data_file:
     admin_name, admin_email = admin_data_file.read().strip().split(',')

ADMINS = [(admin_name, admin_email)]

ALLOWED_HOSTS = []

INTERNAL_IPS = ['127.0.0.1']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'debug_toolbar',
    'rest_framework',
    'django_filters',
    'graphene_django',
    'site_data.apps.SiteDataConfig',
    'my_user.apps.MyUserConfig',
    'course.apps.CourseConfig',
    'course_api.apps.CourseApiConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'learning_platform.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'learning_platform.wsgi.application'

with open('learning_platform/private_data/database_password.txt') as db_password_file:
    db_password = db_password_file.read().strip()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'learning_platform',
        'USER': 'postgres',
        'PASSWORD': db_password,
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

AUTH_USER_MODEL = 'my_user.MyUser'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES':('rest_framework.permissions.IsAuthenticated',),
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication'
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'PAGE_SIZE': 100
}

REST_AUTH_SERIALIZERS = {
    'USER_DETAILS_SERIALIZER':'course_api.serializers.MyUserSerilizer' }

EMAIL_HOST = 'smtp.gmail.com'

EMAIL_HOST_USER = 'courseplatformdj'

with open('learning_platform/private_data/email.txt') as email_password_file:
    email_password = email_password_file.read().strip()

EMAIL_HOST_PASSWORD = email_password

EMAIL_PORT = 587

EMAIL_USE_TLS = True

DEFAULT_FROM_EMAIL = 'Команда Онлайн университета'

DEFAULT_TO_EMAIL = 'courseplatformdj@gmail.com'

REDIS_HOST = 'localhost'

REDIS_PORT = '6379'

BROKER_URL = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/0'

BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}

CELERY_RESULT_BACKEND = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/0'
