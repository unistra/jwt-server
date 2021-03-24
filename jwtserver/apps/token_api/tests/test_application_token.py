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

    def test_get_token(self):
        with patch(
            "jwtserver.apps.token_api.serializers.get_user"
        ) as mock_ldap:
            mock_ldap.return_value = self.get_user_return
            response = self.client.post(
                reverse("token_o_matic"),
                {
                    "token": self.application_token.auth_token,
                    "service": str(self.authorized_service),
                },
                format="json",
            )
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
            self.assertEqual(response.data["service"], str(self.authorized_service))
