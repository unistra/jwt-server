from datetime import timedelta
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

DATABASES['default']['HOST'] = '{{ default_db_host }}'
DATABASES['default']['USER'] = '{{ default_db_user }}'
DATABASES['default']['PASSWORD'] = '{{ default_db_password }}'
DATABASES['default']['NAME'] = '{{ default_db_name }}'

############################
# Allowed hosts & Security #
############################

ALLOWED_HOSTS = [
    '.u-strasbg.fr',
    '.unistra.fr',
]
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTOCOL", "ssl")


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
    dsn="https://5ccdeb9b7d9e4e70a824349302ae43a8@sentry.app.unistra.fr/11",
    integrations=[DjangoIntegration()],
    environment=STAGE,
    release=open(SITE_ROOT / "build.txt", 'r').read()
)


##############
# Encryption #
##############
RSA_PASSWORD = '{{ rsa_password }}'
check_key('myKey.pem', 'SIGNING_KEY', password=RSA_PASSWORD)

#######
# JWT #
#######
JWT_ACCESS_LIFETIME = '{{ jwt_access_lifetime }}'
JWT_REFRESH_LIFETIME = '{{ jwt_refresh_lifetime }}'

SIMPLE_JWT.update(
    {
        'ACCESS_TOKEN_LIFETIME': timedelta(minutes=int(JWT_ACCESS_LIFETIME)),
        'REFRESH_TOKEN_LIFETIME': timedelta(days=int(JWT_REFRESH_LIFETIME)),
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

#####################
#       CAS         #
#####################
CAS_SERVER_URL = 'https://cas-dev.unistra.fr:443/cas/'
