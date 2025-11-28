from os import environ
from pathlib import Path

from .base import *

#######################
# Debug configuration #
#######################

DEBUG = True
STAGE = "unittest"

##########################
# Database configuration #
##########################

DATABASES["default"]["HOST"] = environ.get("DB_HOST", "postgres")
DATABASES["default"]["USER"] = environ.get("TEST_DB_USER", "jwtserver")
DATABASES["default"]["PASSWORD"] = environ.get("DB_PWD", "jwtserver")
DATABASES["default"]["NAME"] = environ.get("DB_NAME", "jwtserver-test")

############################
# Allowed hosts & Security #
############################

ALLOWED_HOSTS = ["*"]

#####################
# Log configuration #
#####################

LOGGING["handlers"]["file"]["filename"] = environ.get(
    "LOG_DIR",
    Path("/tmp").resolve(strict=True) / f"test_{SITE_NAME}.log",
)
LOGGING["handlers"]["file"]["level"] = "DEBUG"

for logger in LOGGING["loggers"]:
    LOGGING["loggers"][logger]["level"] = "DEBUG"

TEST_RUNNER = "django.test.runner.DiscoverRunner"

SIMPLE_JWT = {
    "USER_ID_FIELD": "username",
    "ALGORITHM": "HS256",
    "SIGNING_KEY": "S3creT~KEy",
}

####################
#      VITE        #
####################
DJANGO_VITE["default"]["dev_mode"] = True
