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

###############################
# Weberservices configuration #
###############################

CAMELOTWS_DESCRIPTION = 'https://camelotv2-test-siham.u-strasbg.fr/site_media/description.json'
CAMELOTWS_BASE_URL = 'https://camelotv2-test-siham.u-strasbg.fr'
CAMELOTWS_TOKEN = '{{ camelotws_token }}'


sentry_sdk.init(
    dsn="https://0e41ea754eff4321a9f36c95039f5910@sentry-test.app.unistra.fr/16",
    integrations=[DjangoIntegration()],
    environment="test",
    release=open(path.join(dirname(abspath(__file__)), "../../", "build.txt"), 'r').read()
)
