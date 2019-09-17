# -*- coding: utf-8 -*-

from os import path

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from .base import *

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

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTOCOL', 'ssl')

#####################
# Log configuration #
#####################

LOGGING['handlers']['file']['filename'] = '{{ remote_current_path }}/log/app.log'

##############
# Secret key #
##############

SECRET_KEY = '{{ secret_key }}'

############
# Dipstrap #
############

DIPSTRAP_VERSION = '{{ dipstrap_version }}'
DIPSTRAP_STATIC_URL += '%s/' % DIPSTRAP_VERSION

###############################
# Weberservices configuration #
###############################

CAMELOTWS_DESCRIPTION = 'https://camelotv2-ws.u-strasbg.fr/site_media/description.json'
CAMELOTWS_BASE_URL = 'https://camelotv2-ws.u-strasbg.fr'
CAMELOTWS_TOKEN = '{{ camelotws_token }}'

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
