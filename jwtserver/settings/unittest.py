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
DATABASES['default']['USER'] = environ.get('DB_USER')
DATABASES['default']['PASSWORD'] = environ.get('DB_PWD')
DATABASES['default']['NAME'] = environ.get('DB_NAME')

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

LDAP_PROTOCOL = environ.get('LDAP_PROTOCOL', 'ldap')
LDAP_SERVER = environ.get('LDAP_SERVER')
LDAP_PORT = int(environ.get('LDAP_PORT', 389))
LDAP_CONNEXION = f'{LDAP_PROTOCOL}://{LDAP_SERVER}:{LDAP_PORT}'
LDAP_USER = environ.get('LDAP_USER')
LDAP_PASSWORD = environ.get('LDAP_PASSWORD')
LDAP_BRANCH = environ.get('LDAP_BRANCH', 'ou=people,o=annuaire')
LDAP_FILTER = environ.get('LDAP_FILTER', '(&(udsSourcePresent=TRUE)(uid={}))')

SIMPLE_JWT = {
    'USER_ID_FIELD': 'username',
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': 'S3creT~KEy'
}
