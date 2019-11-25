# -*- coding: utf-8 -*-

from os import path

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from .base import *

#######################
# Debug configuration #
#######################

DEBUG = True


##########################
# Database configuration #
##########################

DATABASES['default']['ENGINE'] = 'django.db.backends.sqlite3'
DATABASES['default']['NAME'] = normpath(join(dirname(dirname(SITE_ROOT)), 'shared/default.db'))

############################
# Allowed hosts & Security #
############################

ALLOWED_HOSTS = [
    '.u-strasbg.fr',
    '.unistra.fr',
]

#####################
# Log configuration #
#####################

LOGGING['handlers']['file']['filename'] = '{{ remote_current_path }}/log/app.log'

for logger in LOGGING['loggers']:
    LOGGING['loggers'][logger]['level'] = 'DEBUG'


############
# Dipstrap #
############

DIPSTRAP_VERSION = '{{ dipstrap_version }}'
DIPSTRAP_STATIC_URL += '%s/' % DIPSTRAP_VERSION

#########
# STAGE #
#########
STAGE = '{{ goal }}'


##########
# Sentry #
##########
sentry_sdk.init(
    dsn="https://0e41ea754eff4321a9f36c95039f5910@sentry-test.app.unistra.fr/16",
    integrations=[DjangoIntegration()],
    environment=STAGE,
    release=open(path.join(dirname(abspath(__file__)), "../../", "build.txt"), 'r').read()
)


##############
# Encryption #
##############
RSA_PASSWORD = '{{ rsa_password }}'
check_key('myKey.pem', 'SIGNING_KEY', password=RSA_PASSWORD)

#######
# JWT #
#######
SIMPLE_JWT.update(
    {
        'ACCESS_TOKEN_LIFETIME': timedelta(minutes=int('{{ jwt_access_lifetime }}')),
        'REFRESH_TOKEN_LIFETIME': timedelta(days=int('{{ jwt_refresh_lifetime }}'))
    }
)


########
# LDAP #
########
LDAP_PROTOCOL = '{{ ldap_protocol }}'
LDAP_SERVER = '{{ ldap_server }}'
LDAP_PORT = '{{ ldap_port }}'
LDAP_CONNEXION = f'{LDAP_PROTOCOL}://{LDAP_SERVER}:{LDAP_PORT}'
LDAP_USER = '{{ ldap_user }}'
LDAP_PASSWORD = '{{ ldap_password }}'
LDAP_BRANCH = '{{ ldap_branch }}'
LDAP_FILTER = '{{ ldap_filter }}'
