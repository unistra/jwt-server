import logging
from functools import wraps

import britney_utils
from britney.errors import SporeMethodCallError, SporeMethodStatusError
from britney.middleware.format import Json
from django.conf import settings

from .exceptions import WSError

_clients = {}


def get_client(name):
    global _clients

    name = name.upper()
    if name not in _clients:
        client = britney_utils.get_client(
            name,
            getattr(settings, '%sWS_DESCRIPTION' % name),
            base_url=getattr(settings, '%sWS_BASE_URL' % name),
            middlewares=(
                (Json,),
                ('ApiKey', {
                    'key_name': 'Authorization',
                    'key_value': 'Token %s' % getattr(
                        settings, '%sWS_TOKEN' % name)
                }),
            )
        )
        client.add_default('format', 'json')
        _clients[name] = client

    return _clients[name]


def check_status(logger_name=__name__):
    def wrapper(func):
        object_type = func.__name__.replace('get_', '').rstrip('s')
        logger = logging.getLogger(logger_name)

        @wraps(func)
        def wrapped(*args, **kwargs):
            logger.debug('Getting %s', object_type)
            try:
                response = func(*args, **kwargs)
            except SporeMethodStatusError as http_error:
                status = http_error.response.status_code
                if status == 401:
                    message = 'Webservice account can\'t authenticate'
                elif status == 403:
                    message = 'Webservice account needs some authorization'
                elif status >= 500:
                    message = 'Webservice seems to be down'
                else:
                    message = 'Error %s' % http_error.response.reason
                logger.critical('%s: %s', status, message)
                raise WSError(http_error.response, message, object_type)
            except SporeMethodCallError as method_call_error:
                message = 'Bad function call: %s' % method_call_error.cause
                logger.critical(message)
                logger.critical('Expected values: %s',
                                ', '.join(method_call_error.expected_values))
                raise WSError(None, message, object_type)
            else:
                logger.debug(response.request.url)
                return response

        return wrapped

    return wrapper


def get_user(username):
    return get_client('camelot').get_persons(username=username)
