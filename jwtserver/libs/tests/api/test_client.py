from unittest.mock import patch

from django.test import override_settings, TestCase

from ...api.client import get_ldap_filter, get_user, UserNotFoundError


@override_settings(LDAP_FILTER="(&(uid={uid}){additional_filters})")
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
            "(&(uid=login)(memberOf=cn=list-name@unistra.fr,ou=groups,o=org)(any other filter))",  # noqa: E501
        )

    def test_additional_filters_can_be_empty(self):
        conditions = {}
        filter = get_ldap_filter("login", conditions)
        self.assertEqual(filter, "(&(uid=login))")

    def test_conditions_may_be_none(self):
        filter = get_ldap_filter("login", conditions=None)
        self.assertEqual(filter, "(&(uid=login))")


@override_settings(
    LDAP_FILTER="(&(uid={uid}){additional_filters})", LDAP_BRANCH=""
)
@patch("jwtserver.libs.api.client.get_client")
class ClientRaisesExceptionOnNoUserFound(TestCase):
    def setUp(self) -> None:
        pass

    def test_no_result_raises_exception(self, client_mock):
        client_mock.return_value.search_s.return_value = []
        with self.assertRaises(UserNotFoundError) as ctx:
            get_user("login", raise_exception=True)
        self.assertEqual(str(ctx.exception), "User <login> not found")
