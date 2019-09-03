# -*- coding: utf-8 -*-

from os import environ, path

from .base import *

#######################
# Debug configuration #
#######################

DEBUG = True


##########################
# Database configuration #
##########################

# In your virtualenv, edit the file $VIRTUAL_ENV/bin/postactivate and set
# properly the environnement variable defined in this file (ie: os.environ[KEY])
# ex: export DEFAULT_DB_NAME='project_name'

# Default values for default database are :
# engine : sqlite3
# name : PROJECT_ROOT_DIR/default.db


DATABASES['default']['ENGINE'] = 'django.db.backends.sqlite3'
DATABASES['default']['NAME'] = 'jwtserver.db'

############################
# Allowed hosts & Security #
############################

ALLOWED_HOSTS = [
    '*'
]

#####################
# Log configuration #
#####################

LOGGING['handlers']['file']['filename'] = environ.get('LOG_DIR',
        normpath(join('/tmp', '%s.log' % SITE_NAME)))
LOGGING['handlers']['file']['level'] = 'DEBUG'

for logger in LOGGING['loggers']:
    LOGGING['loggers'][logger]['level'] = 'DEBUG'


###########################
# Unit test configuration #
###########################

INSTALLED_APPS += [
    'coverage',
    'debug_toolbar',
]

############
# Dipstrap #
############

DIPSTRAP_VERSION = environ.get('DIPSTRAP_VERSION', 'latest')
DIPSTRAP_STATIC_URL += '%s/' % DIPSTRAP_VERSION

#################
# Debug toolbar #
#################

DEBUG_TOOLBAR_PATCH_SETTINGS = False
MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]
INTERNAL_IPS = ['127.0.0.1', '0.0.0.0']

###############################
# Weberservices configuration #
###############################

CAMELOTWS_DESCRIPTION = 'https://camelotv2-test-siham.u-strasbg.fr/site_media/description.json'
CAMELOTWS_BASE_URL = 'https://camelotv2-test-siham.u-strasbg.fr'
CAMELOTWS_TOKEN = environ.get('CAMELOTWS_TOKEN', '{{ camelotws_token }}')

# sentry_sdk.init(
#     dsn="https://0e41ea754eff4321a9f36c95039f5910@sentry-test.app.unistra.fr/16",
#     integrations=[DjangoIntegration()],
#     environment="dev",
#     release=open(path.join(dirname(abspath(__file__)), "../../", "build.txt"), 'r').read()
# )

RSA_PASSWORD = environ.get('RSA_PASSWORD')
check_key('myKey.pem', 'SIGNING_KEY', password=RSA_PASSWORD)
