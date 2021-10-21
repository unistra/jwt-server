import logging

import ldap
from django.conf import settings

from ..decorators import MemoizeWithTimeout

logger = logging.getLogger(__name__)


class UserNotFoundError(ldap.LDAPError):
    pass


@MemoizeWithTimeout(60)
def get_client():
    connexion = ldap.initialize(settings.LDAP_CONNEXION, bytes_mode=False)
    connexion.simple_bind_s(settings.LDAP_USER, settings.LDAP_PASSWORD)
    return connexion


def get_ldap_filter(uid, conditions=None) -> str:
    filters = ""
    if isinstance(conditions, dict) and "ldap_filters" in conditions:
        try:
            filters = "(&" + "".join(
                [f"({filter})" for filter in conditions["ldap_filters"]]
            ) + ")"
        except TypeError:
            # conditions["ldap_filters"] is not iterable ?
            logger.exception("AuthorizedService ldap_filters error.")
            pass
    _filter = settings.LDAP_FILTER.format(uid=uid)
    if filters:
        _filter = f'(&({_filter}){filters})'
    logger.debug(f"LDAP filter {_filter}")

    return _filter


@MemoizeWithTimeout(timeout=86400)
def get_user(username, fields=None, raise_exception=False, conditions=None):
    _filter = get_ldap_filter(username, conditions)

    results = get_client().search_s(
        settings.LDAP_BRANCH, ldap.SCOPE_SUBTREE, _filter
    )

    if isinstance(conditions, dict) and conditions.get(
        "ldap_must_exist", False
    ):
        raise_exception = True

    if len(results) == 0 and raise_exception:
        raise UserNotFoundError(f"User <{username}> not found")

    if len(results) != 1:
        logger.debug(
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
