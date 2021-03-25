import logging

import ldap
import sentry_sdk
from django.conf import settings

from jwtserver.libs.decorators import MemoizeWithTimeout

logger = logging.getLogger(__name__)


class UserNotFoundError(ldap.LDAPError):
    pass


@MemoizeWithTimeout(60)
def get_client():
    connexion = ldap.initialize(settings.LDAP_CONNEXION, bytes_mode=False)
    connexion.simple_bind_s(settings.LDAP_USER, settings.LDAP_PASSWORD)
    return connexion


@MemoizeWithTimeout(timeout=86400)
def get_user(username, fields=None, raise_exception=False):
    results = get_client().search_s(
        settings.LDAP_BRANCH,
        ldap.SCOPE_SUBTREE,
        settings.LDAP_FILTER.format(username),
    )

    if len(results) == 0 and raise_exception:
        raise UserNotFoundError("User not found")

    if len(results) != 1:
        logger.error(
            f"Received {len(results)} results for query on {username}"
        )
        sentry_sdk.capture_message(
            f"Received {len(results)} results for query on {username}"
        )
        return None
    people = results[0]

    def get_attr(attr):
        return people[1][attr][0].decode("utf-8")

    def get_attrs(attr):
        return [x.decode("utf-8") for x in people[1][attr]]

    def get_ordered_attrs(primary_attr, attr):
        return get_attrs(primary_attr) + list(
            set(get_attrs(attr)) - set(get_attrs(primary_attr))
        )

    def get(attr):
        try:
            if isinstance(attr, str):
                return get_attr(attr)
            elif isinstance(attr, list):
                return get_ordered_attrs(attr[0], attr[1])
        except KeyError:
            # Attribute is not available for user
            pass

    return {k: get(v) for k, v in fields.items() if get(v) is not None}
