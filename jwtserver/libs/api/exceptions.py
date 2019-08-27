import logging

from django.utils.translation import ugettext_lazy as _


class LogMessageMixin:

    def log(self, level, message='', logger_name=__name__):
        getattr(
            logging.getLogger(logger_name), level
        )(message or self.message)


class WSError(LogMessageMixin, Exception):

    def __init__(self, response, message, object_type):
        self.response = response
        self.message = message
        self.object_type = object_type
        self.user_message = _('Unable to get information about %ss' %
                              object_type)
