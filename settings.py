# Django settings for placemotion project.
import os.path
import sys

PROJECT_ROOT = os.path.normpath(os.path.dirname(__file__))
DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
         'ENGINE': 'django.db.backends.sqlite3',
         'NAME': 'urbanbike.db',
         'USER': '',
         'PASSWORD': '',
         'HOST': '', 
     }
}

HOST_NAME = 'http://urbanbike.me'
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = False

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static_out')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_ROOT, 'static'),
    os.path.join(PROJECT_ROOT, 'media'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '86=!@a@ls)b2*bwpic5^t#4&2lujlflk^ox5k095yl+$0%sx=v'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

AUTHENTICATION_BACKENDS = (
    'facebook.backend.FacebookBackend', 
    'django.contrib.auth.backends.ModelBackend'
)
AUTH_PROFILE_MODULE = 'checkins.UserProfile'

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
#    'i18n.middleware.LocaleMiddleware',
#    'django.middleware.locale.LocaleMiddleware',
#    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'checkins.middleware.NginxMiddleware',
    'checkins.middleware.TimezoneMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_ROOT, 'templates'),
)
gettext = lambda s: s

LANGUAGES = (
    ('en', gettext('English')),
)

USE_TZ = True

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.localflavor',
    'django.contrib.messages',
    'django.contrib.humanize',
    'facebook',
    'south',
    'checkins',
    'instagram',
    'twitter',
    'cities',
    'django_extensions',
    'sorl.thumbnail',
    'continents',
    'traces',
)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'TIMEOUT': 3600,
    }
}

CITIES_PLUGINS = [
    'cities.plugin.postal_code_ca.Plugin',  # Canada postal codes need region codes remapped to match geonames
]
CITIES_POSTAL_CODES = ['US', 'CA']
CITIES_LOCALES = ['en']

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.contrib.messages.context_processors.messages",
    "checkins.context_processors.development_settings",
)

LOGIN_REDIRECT_URL = '/?locate-me'
# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
            },
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            },
        },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
            },
        'cities': {
            'handlers': ['console'],
            'level': 'INFO',
            },
        }
}

GEOIP_CITY = PROJECT_ROOT + '/data/GeoLiteCity.dat'

# define them in settings_local
GA_UID = ''
GOOGLE_API_KEY = ''

INSTAGRAM_CLIENT_ID = ''
INSTAGRAM_PRIVATE = ''

FACEBOOK_APP_ID = ''
FACEBOOK_APP_SECRET = ''
FACEBOOK_SCOPE = 'email'

MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
HOST_NAME = 'localhost'

try:
    from settings_local import *
except ImportError, exc:
    if str(exc) != 'No module named settings_local':
        raise
