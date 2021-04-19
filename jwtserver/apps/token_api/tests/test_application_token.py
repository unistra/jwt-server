import secrets
from unittest.mock import patch

import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from ..models import ApplicationToken, AuthorizedService


class ApplicationTokenTest(APITestCase):
    def setUp(self) -> None:
        self.authorized_service = AuthorizedService.objects.create(
            data={
                "fields": {
                    "username": "uid",
                    "affiliations": [
                        "eduPersonPrimaryAffiliation",
                        "eduPersonAffiliation",
                    ],
                    "directory_id": "udsDirectoryId",
                    "organization": "supannEtablissement",
                },
                "issuer": "Ernest",
                "service": "test-service.unistra.fr",
            }
        )
        self.application_token = ApplicationToken.objects.create(
            authorized_service=self.authorized_service,
            account="username",
        )
        self.user = get_user_model().objects.create_user("username", "")
        self.get_user_return = {
            "username": "username",
            "affiliations": ["employee", "member"],
            "directory_id": "123456",
            "organization": "ORG",
        }

    def _make_response(self, token=None, service=None):
        if token is None:
            token = self.application_token.auth_token
        if service is None:
            service = str(self.authorized_service)
        response = self.client.post(
            reverse("token_o_matic"),
            {
                "token": token,
                "service": service,
            },
            format="json",
        )
        return response

    @patch("jwtserver.apps.token_api.serializers.get_user")
    def test_get_token(self, get_user_mock):
        get_user_mock.return_value = self.get_user_return
        response = self._make_response()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        access_token = jwt.decode(
            response.data["access"],
            settings.SIMPLE_JWT["SIGNING_KEY"],
            algorithm=settings.SIMPLE_JWT["SIGNING_KEY"],
        )
        self.assertEqual(access_token["user_id"], self.user.username)
        self.assertEqual(access_token["username"], self.user.username)
        self.assertEqual(
            access_token["iss"], self.authorized_service.data["issuer"]
        )
        self.assertEqual(
            response.data["service"], str(self.authorized_service)
        )

    @patch("jwtserver.apps.token_api.serializers.get_user")
    def test_only_access_token_is_returned(self, get_user_mock):
        get_user_mock.return_value = self.get_user_return
        response = self._make_response()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(list(response.data.keys()), ["service", "access"])

    def test_invalid_token_raises_permission_denied(self):
        response = self._make_response(token=secrets.token_urlsafe(50))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data["detail"], "invalid_token")

    def test_invalid_service_raises_permission_denied(self):
        response = self._make_response(
            service="non-existent-service.unistra.fr"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data["detail"], "invalid_service")

    def test_service_and_token_must_match(self):
        other_service = AuthorizedService.objects.create(
            data={"fields": {}, "service": "other-service.unistra.fr"}
        )
        response = self._make_response(service=str(other_service))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data["detail"], "invalid_token")

    def test_non_existent_user_returns_not_found_error(self):
        self.application_token.account = "non-existent-user"
        self.application_token.save()
        response = self._make_response()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @patch("jwtserver.libs.api.client.get_client")
    def test_non_existent_ldap_user_returns_not_found_error(self, client_mock):
        with self.settings(LDAP_BRANCH="", LDAP_FILTER=""):
            client_mock.return_value.search_s.return_value = []
            response = self._make_response()
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_method_is_not_allowed(self):
        response = self.client.get(reverse("token_o_matic"))
        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED
        )
