from pathlib import Path
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

######################
# Path configuration #
######################

DJANGO_ROOT = Path(__file__).resolve(strict=True).parent.parent
SITE_ROOT = DJANGO_ROOT.parent
SITE_NAME = DJANGO_ROOT.name
JSONSCHEMA_ROOT = DJANGO_ROOT / "apps/token_api/schemas"

#######################
# Debug configuration #
#######################

DEBUG = False
TEMPLATE_DEBUG = DEBUG

##########################
# Manager configurations #
##########################

ADMINS = [
    # ('Your Name', 'your_email@example.com'),
]

MANAGERS = ADMINS

##########################
# Database configuration #
##########################

# In your virtualenv, edit the file $VIRTUAL_ENV/bin/postactivate and set
# properly the environnement variable defined in this file (ie: os.environ[KEY])
# ex: export DEFAULT_DB_USER='jwtserver'

# Default values for default database are :
# engine : sqlite3
# name : PROJECT_ROOT_DIR/jwtserver.db

# defaut db connection
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'jwtserver',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '5432',
    }
}

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

######################
# Site configuration #
######################

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.11/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

#########################
# General configuration #
#########################

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Paris'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'fr-FR'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

#######################
# locale configuration #
#######################

LOCALE_PATHS = [
    DJANGO_ROOT / 'locale',
]

#######################
# Media configuration #
#######################

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = DJANGO_ROOT / 'media'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'

##############################
# Static files configuration #
##############################

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = SITE_ROOT / 'assets'

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/site_media/'

# Additional locations of static files
STATICFILES_DIRS = [
    DJANGO_ROOT / 'static',
]

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

############
# Dipstrap #
############

DIPSTRAP_STATIC_URL = '//django-static.u-strasbg.fr/dipstrap/'

##############
# Secret key #
##############

# Make this unique, and don't share it with anybody.
# Only for dev and test environnement. Should be redefined for production
# environnement
SECRET_KEY = 'ma8r116)33!-#pty4!sht8tsa(1bfe%(+!&9xfack+2e9alah!'

##########################
# Template configuration #
##########################

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
            ],
        },
    },
]

############################
# Middleware configuration #
############################

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_cas.middleware.CASMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

#####################
# Url configuration #
#####################

ROOT_URLCONF = '%s.urls' % SITE_NAME

######################
# WSGI configuration #
######################

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = '%s.wsgi.application' % SITE_NAME

#############################
# Application configuration #
#############################

DJANGO_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin'
    # 'django.contrib.admindocs',
]

THIRD_PARTY_APPS = [
    'django_cas',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
]

LOCAL_APPS = [
    'jwtserver',
    'jwtserver.apps.token_api',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

#########################
# Session configuration #
#########################

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

#####################
# Log configuration #
#####################

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(levelname)s %(asctime)s %(name)s:%(lineno)s %(message)s'
        },
        'django.server': {
            '()': 'django.utils.log.ServerFormatter',
            'format': '[%(server_time)s] %(message)s',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        },
        'django.server': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'django.server',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '',
            'maxBytes': 209715200,
            'backupCount': 3,
            'formatter': 'default'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'mail_admins'],
            'level': 'INFO',
        },
        'django.server': {
            'handlers': ['django.server'],
            'level': 'INFO',
            'propagate': False,
        },
        'jwtserver': {
            'handlers': ['mail_admins', 'file'],
            'level': 'ERROR',
            'propagate': True
        }
    }
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication'
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )
}

#####################
#       CAS         #
#####################
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'django_cas.backends.CASBackend',
)

CAS_SERVER_URL = 'https://cas.unistra.fr:443/cas/'
CAS_LOGOUT_REQUEST_ALLOWED = ('cas1.di.unistra.fr', 'cas2.di.unistra.fr')
CAS_LOGOUT_COMPLETELY = True
CAS_USER_CREATION = True
CAS_IGNORE_REFERER = True
CAS_RETRY_LOGIN = True
CAS_USERNAME_FORMAT = lambda username: username.lower().strip()

CAS_FORCE_SSL_SERVICE_URL = True

CAS_ADMIN_AUTH = True
CAS_ADMIN_PREFIX = '/admin/'

SIMPLE_JWT = {
    'USER_ID_FIELD': 'username',
    'ALGORITHM': 'RS256',
}

##############
# Encryption #
##############


def check_key(filename, key_type, **kwargs):
    full_path = SITE_ROOT / 'keys' / filename
    if full_path.is_file():
        if key_type == 'SIGNING_KEY':
            with open(full_path, "rb") as key_file:
                # Read key with passphrase
                if 'password' not in kwargs:
                    raise ValueError("No password provided for private key")
                private_key = serialization.load_pem_private_key(
                    key_file.read(),
                    password=kwargs['password'].encode(),
                    backend=default_backend()
                )

                SIMPLE_JWT[key_type] = private_key
                key_file.close()
        else:
            key_file = open(full_path, 'rb')
            SIMPLE_JWT[key_type] = key_file.read()
            key_file.close()


check_key('myPublic.pem', 'VERIFYING_KEY')


#####################
#       CORS        #
#####################

CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = ('http://localhost:8080',)
CORS_ALLOW_CREDENTIALS = True

####################
#      VITE        #
####################
DJANGO_VITE = {
    "default": {
        "dev_mode": False,
        "static_url_prefix": "dist/",
        "manifest_path": DJANGO_ROOT / "jwtserver" / "static" / "dist" / "manifest.json",
    },
}