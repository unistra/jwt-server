from datetime import timedelta
from os import environ

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


DATABASES['default']['HOST'] = environ.get("DB_HOST", "localhost")
DATABASES['default']['USER'] = environ.get("DB_USER", "jwtserver")
DATABASES['default']['PASSWORD'] = environ.get("DB_PWD", "jwtserver")
DATABASES['default']['NAME'] = environ.get("DB_NAME", "jwtserver")

############################
# Allowed hosts & Security #
############################

ALLOWED_HOSTS = [
    '*'
]

#####################
# Log configuration #
#####################

LOGGING['handlers']['file']['filename'] = environ.get(
    'LOG_DIR',
    Path('/tmp').resolve(strict=True) / f'{SITE_NAME}.log',
)
LOGGING['handlers']['file']['level'] = 'DEBUG'

for logger in LOGGING['loggers']:
    LOGGING['loggers'][logger]['level'] = 'DEBUG'

###########################
# Unit test configuration #
###########################

INSTALLED_APPS += [
    'coverage',
    'debug_toolbar',
    'django_extensions',
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

# sentry_sdk.init(
#     dsn="https://0e41ea754eff4321a9f36c95039f5910@sentry-test.app.unistra.fr/16",
#     integrations=[DjangoIntegration()],
#     environment="dev",
#     release=open(path.join(dirname(abspath(__file__)), "../../", "build.txt"), 'r').read()
# )

RSA_PASSWORD = environ.get('RSA_PASSWORD')
check_key('myKey.pem', 'SIGNING_KEY', password=RSA_PASSWORD)

#########
# STAGE #
#########
STAGE = 'dev'

#######
# JWT #
#######
SIMPLE_JWT.update(
    {
        'ACCESS_TOKEN_LIFETIME': timedelta(minutes=int(environ.get('JWT_ACCESS_LIFETIME'))),
        'REFRESH_TOKEN_LIFETIME': timedelta(days=int(environ.get('JWT_REFRESH_LIFETIME')))
    }
)

########
# LDAP #
########
LDAP_PROTOCOL = environ.get('LDAP_PROTOCOL', 'ldap')
LDAP_SERVER = environ.get('LDAP_SERVER')
LDAP_PORT = int(environ.get('LDAP_PORT', 389))
LDAP_CONNEXION = f'{LDAP_PROTOCOL}://{LDAP_SERVER}:{LDAP_PORT}'
LDAP_USER = environ.get('LDAP_USER')
LDAP_PASSWORD = environ.get('LDAP_PASSWORD')
LDAP_BRANCH = environ.get('LDAP_BRANCH', 'ou=people,o=annuaire')
LDAP_FILTER = environ.get(
    'LDAP_FILTER',
    'uid={uid}'
)

#####################
#       CAS         #
#####################
CAS_SERVER_URL = 'https://cas-dev.unistra.fr:443/cas/'
CAS_FORCE_SSL_SERVICE_URL = False

####################
#      VITE        #
####################
DJANGO_VITE["default"]["dev_mode"] = True
