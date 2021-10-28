from unittest.mock import patch

from django.test import override_settings, TestCase

from ...api import client
from ...api.client import get_ldap_filter, get_user, UserNotFoundError


@override_settings(LDAP_FILTER="uid={uid}")
class LdapFilterTest(TestCase):
    def setUp(self) -> None:
        self.conditions = {
            "ldap_filters": [
                "memberOf=cn=list-name@unistra.fr,ou=groups,o=org",
                "any other filter",
            ],
            "callbacks": [""],
        }

    def test_additional_filters_are_added_to_ldap_filter(self):
        filter = get_ldap_filter("login", self.conditions)
        self.assertEqual(
            filter,
            "(&(uid=login)(&(memberOf=cn=list-name@unistra.fr,ou=groups,o=org)(any other filter)))",  # noqa: E501
        )

    def test_additional_filters_can_be_empty(self):
        conditions = {}
        filter = get_ldap_filter("login", conditions)
        self.assertEqual(filter, "uid=login")

    def test_conditions_may_be_none(self):
        filter = get_ldap_filter("login", conditions=None)
        self.assertEqual(filter, "uid=login")

    def test_error_is_logged_when_ldap_filters_is_not_iterable(self):
        with self.assertLogs(client.__name__) as ctx:
            filter = get_ldap_filter("login", conditions={"ldap_filters": 12})
            self.assertEqual("uid=login", filter)
            self.assertIn("ldap_filters error", str(ctx.output))


@override_settings(
    LDAP_FILTER="uid={uid}", LDAP_BRANCH=""
)
@patch("jwtserver.libs.api.client.get_client")
class ClientRaisesExceptionOnNoUserFound(TestCase):
    def test_no_result_raises_exception(self, client_mock):
        client_mock.return_value.search_s.return_value = []
        with self.assertRaises(UserNotFoundError) as ctx:
            get_user("login", raise_exception=True)
        self.assertEqual(str(ctx.exception), "User <login> not found")

    def test_no_result_and_ldap_must_exist_condition_raises_exception(
        self, client_mock
    ):
        client_mock.return_value.search_s.return_value = []
        with self.assertRaises(UserNotFoundError) as ctx:
            get_user(
                "login",
                raise_exception=False,
                conditions={"ldap_must_exist": True},
            )
        self.assertEqual(str(ctx.exception), "User <login> not found")

    def test_no_result_and_ldap_must_exist_not_in_condition_returns_none(
        self, client_mock
    ):
        client_mock.return_value.search_s.return_value = []
        result = get_user("login", raise_exception=None, conditions={})
        self.assertIsNone(result)

    def test_no_result_and_no_conditions_returns_none(self, client_mock):
        client_mock.return_value.search_s.return_value = []
        result = get_user("login")
        self.assertIsNone(result)
