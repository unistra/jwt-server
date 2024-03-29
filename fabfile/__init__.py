from os.path import join

import pydiploy
from fabric.api import env, execute, roles, task

from . import sentry

# edit config here !

env.remote_owner = 'django'  # remote server user
env.remote_group = 'di'  # remote server group

env.application_name = 'jwtserver'   # name of webapp
env.root_package_name = 'jwtserver'  # name of app in webapp

env.remote_home = '/home/django'  # remote home root
env.remote_python_version = '3.9'  # python version
env.remote_virtualenv_root = join(env.remote_home, '.virtualenvs')  # venv root
env.remote_virtualenv_dir = join(env.remote_virtualenv_root,
                                 env.application_name)  # venv for webapp dir
# git repository url
env.remote_repo_url = 'git@git.unistra.fr:di/jwt-server.git'  # 'git@git.net:jwtserver.git'
env.local_tmp_dir = '/tmp'  # tmp dir
env.remote_static_root = '/var/www/static/'  # root of static files
env.locale = 'fr_FR.UTF-8'  # locale to use on remote
env.timezone = 'Europe/Paris'  # timezone for remote
env.keep_releases = 3  # number of old releases to keep before cleaning
env.extra_goals = ['preprod']  # add extra goal(s) to defaults (test,dev,prod)
env.dipstrap_version = 'latest'
env.verbose_output = True  # True for verbose output

# optional parameters

# env.dest_path = '' # if not set using env_local_tmp_dir
# env.excluded_files = ['pron.jpg'] # file(s) that rsync should exclude when deploying app
# env.extra_ppa_to_install = ['ppa:vincent-c/ponysay'] # extra ppa source(s) to use
# env.extra_pkg_to_install = ['ponysay'] # extra debian/ubuntu package(s) to install on remote
# env.cfg_shared_files = ['config','/app/path/to/config/config_file'] # config files to be placed in shared config dir
env.extra_symlink_dirs = ['keys',] # dirs to be symlinked in shared directory
# env.verbose = True # verbose display for pydiploy default value = True
# env.req_pydiploy_version = "0.9" # required pydiploy version for this fabfile
# env.no_config_test = False # avoid config checker if True
# env.maintenance_text = "" # add a customize maintenance text for maintenance page
# env.maintenance_title = "" # add a customize title for maintenance page
# env.oracle_client_version = '11.2'
# env.oracle_download_url = 'http://librepo.net/lib/oracle/'
# env.oracle_remote_dir = 'oracle_client'
# env.oracle_packages = ['instantclient-basic-linux-x86-64-11.2.0.2.0.zip',
#                        'instantclient-sdk-linux-x86-64-11.2.0.2.0.zip',
#                        'instantclient-sqlplus-linux-x86-64-11.2.0.2.0.zip']
#
# env.circus_package_name = 'https://github.com/morganbohn/circus/archive/master.zip'
# env.no_circus_web = True
# env.circus_backend = 'gevent' # name of circus backend to use

# name of chaussette backend to use. You need to add this backend in the app requirement file:
env.chaussette_backend = 'waitress'

# add directive(s) to nginx config file in location part:
# env.nginx_location_extra_directives = ['proxy_read_timeout 120']

# env.nginx_start_confirmation = True # if True when nginx is not started
# needs confirmation to start it.

# Don't declare full_preprod as env.application_name will make declare_release fail
env.releases_to_declare_to_sentry = [
    "test",
    "preprod",
    "prod",
]


@task
def dev():
    """Define dev stage"""
    env.roledefs = {
        'web': ['192.168.1.2'],
        'lb': ['192.168.1.2'],
    }
    env.user = 'vagrant'
    env.backends = env.roledefs['web']
    env.server_name = 'jwtserver-dev.net'
    env.short_server_name = 'jwtserver-dev'
    env.static_folder = '/site_media/'
    env.server_ip = '192.168.1.2'
    env.no_shared_sessions = False
    env.server_ssl_on = False
    env.goal = 'dev'
    env.socket_port = '8001'
    env.map_settings = {}
    execute(build_env)


@task
def test():
    """Define test stage"""
    env.roledefs = {
        'web': ['jwtserver-test.u-strasbg.fr'],
        'lb': ['jwtserver-test.u-strasbg.fr'],
    }
    env.user = 'root'  # user for ssh
    env.backends = ['127.0.0.1']
    env.server_name = 'jwtserver-test.app.unistra.fr'
    env.short_server_name = 'jwtserver-test'
    env.static_folder = '/site_media/'
    env.server_ip = ''
    env.no_shared_sessions = False
    env.server_ssl_on = True
    env.path_to_cert = '/etc/ssl/certs/mega_wildcard.pem'
    env.path_to_cert_key = '/etc/ssl/private/mega_wildcard.key'
    env.goal = 'test'
    env.socket_port = '8036'
    env.socket_host = '127.0.0.1'
    env.map_settings = {
        'default_db_host': "DATABASES['default']['HOST']",
        'default_db_user': "DATABASES['default']['USER']",
        'default_db_password': "DATABASES['default']['PASSWORD']",
        'default_db_name': "DATABASES['default']['NAME']",
        'rsa_password': "RSA_PASSWORD",
        'jwt_access_lifetime': 'JWT_ACCESS_LIFETIME',
        'jwt_refresh_lifetime': 'JWT_REFRESH_LIFETIME',
        'ldap_protocol': 'LDAP_PROTOCOL',
        'ldap_server': 'LDAP_SERVER',
        'ldap_port': 'LDAP_PORT',
        'ldap_user': 'LDAP_USER',
        'ldap_password': 'LDAP_PASSWORD',
        'ldap_branch': 'LDAP_BRANCH',
        'ldap_filter': 'LDAP_FILTER'
    }
    execute(build_env)


@task
def preprod():
    """Define preprod stage"""
    env.roledefs = {
        'web': ['django-pprd-w3.di.unistra.fr', 'django-pprd-w4.di.unistra.fr'],
        'lb': ['rp-dip-pprd-public.di.unistra.fr'],
    }
    # env.user = 'root'  # user for ssh
    env.backends = env.roledefs['web']
    env.server_name = 'jwtserver-pprd.app.unistra.fr'
    env.short_server_name = 'jwtserver-pprd'
    env.static_folder = '/site_media/'
    env.server_ip = '130.79.245.212'
    env.no_shared_sessions = False
    env.server_ssl_on = True
    env.path_to_cert = '/etc/ssl/certs/mega_wildcard.pem'
    env.path_to_cert_key = '/etc/ssl/private/mega_wildcard.key'
    env.goal = 'preprod'
    env.socket_port = '8019'
    env.map_settings = {
        'default_db_host': "DATABASES['default']['HOST']",
        'default_db_user': "DATABASES['default']['USER']",
        'default_db_password': "DATABASES['default']['PASSWORD']",
        'default_db_name': "DATABASES['default']['NAME']",
        'secret_key': "SECRET_KEY",
        'rsa_password': "RSA_PASSWORD",
        'jwt_access_lifetime': 'JWT_ACCESS_LIFETIME',
        'jwt_refresh_lifetime': 'JWT_REFRESH_LIFETIME',
        'ldap_protocol': 'LDAP_PROTOCOL',
        'ldap_server': 'LDAP_SERVER',
        'ldap_port': 'LDAP_PORT',
        'ldap_user': 'LDAP_USER',
        'ldap_password': 'LDAP_PASSWORD',
        'ldap_branch': 'LDAP_BRANCH',
        'ldap_filter': 'LDAP_FILTER',
        'cas_server_url': 'CAS_SERVER_URL',
    }
    execute(build_env)

@task
def full_preprod():
    """Define preprod stage"""
    # Specific content
    env.application_name = 'jwtserver-2'  # name of webapp

    env.roledefs = {
        'web': ['django-pprd-w3.di.unistra.fr', 'django-pprd-w4.di.unistra.fr'],
        'lb': ['rp-dip-pprd-public.di.unistra.fr'],
    }
    # env.user = 'root'  # user for ssh
    env.backends = env.roledefs['web']
    env.server_name = 'jwtserver-pprd-full.app.unistra.fr'
    env.short_server_name = 'jwtserver-pprd'
    env.static_folder = '/site_media/'
    env.server_ip = '130.79.245.212'
    env.no_shared_sessions = False
    env.server_ssl_on = True
    env.path_to_cert = '/etc/ssl/certs/mega_wildcard.pem'
    env.path_to_cert_key = '/etc/ssl/private/mega_wildcard.key'
    env.goal = 'preprod'
    env.socket_port = '8046'
    env.map_settings = {
        'default_db_host': "DATABASES['default']['HOST']",
        'default_db_user': "DATABASES['default']['USER']",
        'default_db_password': "DATABASES['default']['PASSWORD']",
        'default_db_name': "DATABASES['default']['NAME']",
        'secret_key': "SECRET_KEY",
        'rsa_password': "RSA_PASSWORD",
        'jwt_access_lifetime': 'JWT_ACCESS_LIFETIME',
        'jwt_refresh_lifetime': 'JWT_REFRESH_LIFETIME',
        'ldap_protocol': 'LDAP_PROTOCOL',
        'ldap_server': 'LDAP_SERVER',
        'ldap_port': 'LDAP_PORT',
        'ldap_user': 'LDAP_USER',
        'ldap_password': 'LDAP_PASSWORD',
        'ldap_branch': 'LDAP_BRANCH',
        'ldap_filter': 'LDAP_FILTER',
        'cas_server_url': 'CAS_SERVER_URL',
    }
    execute(build_env)


@task
def prod():
    """Define prod stage"""
    env.roledefs = {
        'web': ['django-w7.di.unistra.fr', 'django-w8.di.unistra.fr'],
        'lb': ['rp-dip-public-m.di.unistra.fr', 'rp-dip-public-s.di.unistra.fr']
    }
    # env.user = 'root'  # user for ssh
    env.backends = env.roledefs['web']
    env.server_name = 'jwtserver.app.unistra.fr'
    env.short_server_name = 'jwtserver'
    env.static_folder = '/site_media/'
    env.server_ip = '130.79.245.214'
    env.no_shared_sessions = False
    env.server_ssl_on = True
    env.path_to_cert = '/etc/ssl/certs/mega_wildcard.pem'
    env.path_to_cert_key = '/etc/ssl/private/mega_wildcard.key'
    env.goal = 'prod'
    env.socket_port = '8036'
    env.map_settings = {
        'default_db_host': "DATABASES['default']['HOST']",
        'default_db_user': "DATABASES['default']['USER']",
        'default_db_password': "DATABASES['default']['PASSWORD']",
        'default_db_name': "DATABASES['default']['NAME']",
        'secret_key': "SECRET_KEY",
        'rsa_password': "RSA_PASSWORD",
        'jwt_access_lifetime': 'JWT_ACCESS_LIFETIME',
        'jwt_refresh_lifetime': 'JWT_REFRESH_LIFETIME',
        'ldap_protocol': 'LDAP_PROTOCOL',
        'ldap_server': 'LDAP_SERVER',
        'ldap_port': 'LDAP_PORT',
        'ldap_user': 'LDAP_USER',
        'ldap_password': 'LDAP_PASSWORD',
        'ldap_branch': 'LDAP_BRANCH',
        'ldap_filter': 'LDAP_FILTER'
    }
    execute(build_env)

# dont touch after that point if you don't know what you are doing !


@task
def tag(version_number):
    """ Set the version to deploy to `version_number`. """
    execute(pydiploy.prepare.tag, version=version_number)


@roles(['web', 'lb'])
def build_env():
    execute(pydiploy.prepare.build_env)


@task
def pre_install():
    """Pre install of backend & frontend"""
    execute(pre_install_backend)
    execute(pre_install_frontend)


@roles('web')
@task
def pre_install_backend():
    """Setup server for backend"""
    execute(pydiploy.django.pre_install_backend, commands='/usr/bin/rsync')


@roles('lb')
@task
def pre_install_frontend():
    """Setup server for frontend"""
    execute(pydiploy.django.pre_install_frontend)


@task
def deploy(update_pkg=False):
    """Deploy code on server"""
    execute(deploy_backend, update_pkg)
    execute(declare_release_to_sentry)
    execute(deploy_frontend)


@roles('web')
@task
def deploy_backend(update_pkg=False):
    """Deploy code on server"""
    execute(pydiploy.django.deploy_backend, update_pkg)


@task
def declare_release_to_sentry():
    if env.goal in env.releases_to_declare_to_sentry and env.application_name != "jwtserver-2":
        execute(sentry.declare_release)


@roles('lb')
@task
def deploy_frontend():
    """Deploy static files on load balancer"""
    execute(pydiploy.django.deploy_frontend)


@roles('web')
@task
def rollback():
    """Rollback code (current-1 release)"""
    execute(pydiploy.django.rollback)


@task
def post_install():
    """post install for backend & frontend"""
    execute(post_install_backend)
    execute(post_install_frontend)


@roles('web')
@task
def post_install_backend():
    """Post installation of backend"""
    execute(pydiploy.django.post_install_backend)


@roles('lb')
@task
def post_install_frontend():
    """Post installation of frontend"""
    execute(pydiploy.django.post_install_frontend)


@roles('web')
@task
def install_postgres(user=None, dbname=None, password=None):
    """Install Postgres on remote"""
    execute(pydiploy.django.install_postgres_server,
            user=user, dbname=dbname, password=password)


@task
def reload():
    """Reload backend & frontend"""
    execute(reload_frontend)
    execute(reload_backend)


@roles('lb')
@task
def reload_frontend():
    execute(pydiploy.django.reload_frontend)


@roles('web')
@task
def reload_backend():
    execute(pydiploy.django.reload_backend)


@roles('lb')
@task
def set_down():
    """ Set app to maintenance mode """
    execute(pydiploy.django.set_app_down)


@roles('lb')
@task
def set_up():
    """ Set app to up mode """
    execute(pydiploy.django.set_app_up)


@roles('web')
@task
def custom_manage_cmd(cmd):
    """ Execute custom command in manage.py """
    execute(pydiploy.django.custom_manage_command, cmd)
