import dj_database_url
from decouple import Csv, config
from unipath import Path

PROJECT_DIR = Path(__file__).parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'pharos',
        'USER': 'pharosuser',
        'PASSWORD': '',
        'HOST': '127.0.0.1',  # Or an IP Address that your DB is hosted on
        'PORT': '5432',
    }
}

ALLOWED_HOSTS = ['*']

BASE_URL = "https://127.0.0.1:8000"

# Application definition


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.admin',
    'django.contrib.sites',  # needed for allauth
    'floppyforms',
    'bootcamp.activities',
    'bootcamp.projects',
    'bootcamp.samples',
    'bootcamp.devices',
    'bootcamp.authentication',
    'bootcamp.scanner',
    # 'bootcamp.labs',
    'bootcamp.core',
    'bootcamp.feeds',
    'bootcamp.messenger',
    'bootcamp.questions',
    'bootcamp.search',
    'online_status',
    'django_summernote',
    'multiupload',
    'sslserver',
    # all auth for dropbox only now
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # 'allauth.socialaccount.providers.dropbox',
    'allauth.socialaccount.providers.dropbox_oauth2',

)

SITE_ID = 1

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'online_status.middleware.OnlineStatusMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'bootcamp.urls'

WSGI_APPLICATION = 'bootcamp.wsgi.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            PROJECT_DIR.child('templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'debug': DEBUG
        },
    },
]

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LANGUAGES = (
    ('en', 'English'),
    ('pt-br', 'Portuguese'),
    ('es', 'Spanish')
)

LOCALE_PATHS = (PROJECT_DIR.child('locale'),)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_ROOT = PROJECT_DIR.parent.child('staticfiles')
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    PROJECT_DIR.child('static'),
)

MEDIA_ROOT = PROJECT_DIR.parent.child('media')
MEDIA_URL = '/media/'

LOGIN_URL = '/'
LOGIN_REDIRECT_URL = '/feeds/'

ALLOWED_SIGNUP_DOMAINS = ['*']

FILE_UPLOAD_TEMP_DIR = '/tmp/'
FILE_UPLOAD_PERMISSIONS = 0o644

USERS_ONLINE__TIME_IDLE = 1  # 1 second
USERS_ONLINE__TIME_OFFLINE = 1  # 1 second

LINKEDIN_TOKEN = '78pxbqt7x3s1jx'
LINKEDIN_SECRET = 'Yht3OP3IrIBMoZKL'

DROPBOX_CONSUMER_KEY = 'wyio74zq5zpqdaw'
DROPBOX_CONSUMER_SECRET = 'xgh6ba95z9j3jcz'
DROPBOX_ACCESS_TOKEN = 'xxx'
DROPBOX_ACCESS_TOKEN_SECRET = 'xxx'
