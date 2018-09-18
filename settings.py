# Django settings for mloss project.

VERSION = "v0.1.1"
PRODUCTION = False # set to True when project goes live

if not PRODUCTION:
    DEBUG = True
    TEMPLATE_DEBUG = DEBUG
else:
    DEBUG = False
DEBUG = True

ADMINS = (
    ('Mikio Braun', 'mikio@cs.tu-berlin.de'),
    ('Cheng Soon Ong', 'chengsoon.ong@unimelb.edu.au'),
    ('Soeren Sonnenburg', 'soeren.sonnenburg@tu-berlin.de'),
)

MANAGERS = ADMINS

R_CRAN_BOT = 'r-cran-robot'

if PRODUCTION:
    DATABASES = {
    'default': {
        'NAME': 'DB',
        'ENGINE': 'django.db.backends.mysql',
        'USER': 'DBUSER',
        'PASSWORD': 'DBPW',
    	}
    }
else:
    DATABASES = {
    'default': {
        'NAME': 'mloss',
	'ENGINE': 'django.db.backends.mysql',
        #'ENGINE': 'django.db.backends.sqlite3',
	'USER': 'mloss',
	'PASSWORD': 'xxxxxxx',
	'HOST': '',
	'PORT': '',
    	}
    }



LOGIN_REDIRECT_URL='/'
ACCOUNT_ACTIVATION_DAYS=1
DEFAULT_FROM_EMAIL='mloss@mloss.org'


# send email from this address
SERVER_EMAIL = DEFAULT_FROM_EMAIL

# Local time zone for this installation. Choices can be found here:
# http://www.postgresql.org/docs/8.1/static/datetime-keywords.html#DATETIME-TIMEZONE-SET-TABLE
# although not all variations may be possible on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Berlin'

# Language code for this installation. All choices can be found here:
# http://www.w3.org/TR/REC-html40/struct/dirlang.html#langcodes
# http://blogs.law.harvard.edu/tech/stories/storyReader$15
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
if PRODUCTION:
    MEDIA_ROOT = '/home/mloss/static/media/'
else:
    MEDIA_ROOT = 'media/'

# URL that handles the media served from MEDIA_ROOT.
# Example: "http://media.lawrence.com"
MEDIA_URL = '/media/'

# max size of files that can be uploaded in KB (10M, 200K)
MAX_FILE_UPLOAD_SIZE = 10240
MAX_IMAGE_UPLOAD_SIZE = 200
MAX_IMAGE_UPLOAD_WIDTH = 1280
MAX_IMAGE_UPLOAD_HEIGHT = 1024

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media_admin/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'secret_key'


MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.admindocs.middleware.XViewMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
)


ROOT_URLCONF = 'urls'




import os

if PRODUCTION:
    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': '/home/mloss/django/mloss/templates/',
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',

                ],
                'loaders': [
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                ]
            },
        },
    ]
else:
    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [os.path.join(os.path.dirname(__file__), 'templates/')],
            'OPTIONS': {
                'debug': DEBUG,
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
                'loaders': [
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                ]
            },
        },
    ]


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'registration',
    'django.contrib.admin',
    'django_comments',
    'django.contrib.syndication',
    'django.contrib.flatpages',
    'django.contrib.humanize',
    'software',
    'revision',
    'community',
    'forshow',
    'user',
    'subscriptions2',
    'aggregator',
    'blog',
    'captcha',
    'snowpenguin.django.recaptcha2',
    'markup_deprecated',
)

RECAPTCHA_PUBLIC_KEY = 'recaptcha_public_key'
RECAPTCHA_PRIVATE_KEY = 'recaptcha_private_key'
