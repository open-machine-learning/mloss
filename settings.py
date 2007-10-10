# Django settings for mloss project.

PRODUCTION = False # set to True when project goes live

if not PRODUCTION:
	DEBUG = True
	TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Mikio Braun', 'mikio@cs.tu-berlin.de'),
    ('Cheng Soon Ong', 'chengsoon.ong@tuebingen.mpg.de'),
    ('Soeren Sonnenburg', 'soeren.sonnenburg@first.fraunhofer.de'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'ado_mssql'.
if PRODUCTION:
    DATABASE_NAME = '/home/mloss/mloss/mloss.db'             # Or path to database file if using sqlite3.
else:
    DATABASE_NAME = 'mloss.db'             # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.


LOGIN_REDIRECT_URL='/'
ACCOUNT_ACTIVATION_DAYS=1
DEFAULT_FROM_EMAIL='admin@mloss.org'
EMAIL_HOST='mailhost.tuebingen.mpg.de'

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
    MEDIA_ROOT = '/home/mloss/mloss/media/'
else:
    MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT.
# Example: "http://media.lawrence.com"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
if PRODUCTION:
    ADMIN_MEDIA_PREFIX = 'http://zut.tuebingen.mpg.de/admin_media/'
else:
    ADMIN_MEDIA_PREFIX = '/media_admin/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'ccku5%_-8r2#*rb(yh)j!11ar12vx_tll5u(11%3l=^k8rfe=y'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
	'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
)

ROOT_URLCONF = 'mloss.urls'


#import os.path
TEMPLATE_DIRS = (
    'templates/',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.comments',
    'django.contrib.markup',
    'django.contrib.syndication',
	'django.contrib.flatpages',
	'django.contrib.humanize',
	'mloss',
	'mloss.software',
	'mloss.registration',
	'mloss.community',
	'mloss.forshow',
)
