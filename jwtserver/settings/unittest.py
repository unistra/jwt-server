# -*- coding: utf-8 -*-

from os import environ
from os.path import normpath
from .base import *

#######################
# Debug configuration #
#######################

DEBUG = True

##########################
# Database configuration #
##########################

DATABASES['default']['HOST'] = environ.get('DB_HOST')
DATABASES['default']['USER'] = "postgres"
DATABASES['default']['PASSWORD'] = environ.get('DB_PWD')
DATABASES['default']['NAME'] = environ.get('TEST_DB_NAME')

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
        normpath(join('/tmp', 'test_%s.log' % SITE_NAME)))
LOGGING['handlers']['file']['level'] = 'DEBUG'

for logger in LOGGING['loggers']:
    LOGGING['loggers'][logger]['level'] = 'DEBUG'

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

SIMPLE_JWT = {
    'USER_ID_FIELD': 'username',
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': 'S3creT~KEy'
}
