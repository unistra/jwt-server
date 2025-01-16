import base64
from pathlib import Path
from unittest.mock import patch

import jwt
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from jwtserver.apps.token_api.models import AuthorizedService
from jwtserver.apps.token_api.utils import ExtendedRefreshToken
from jwtserver.libs.api.client import LDAPUserNotFoundError

FIXTURES_ROOT = Path(__file__).resolve(strict=True).parent / "keys/"


class RefreshTokenViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="username",
            email="username@unistra.fr",
        )

        key_file = open(FIXTURES_ROOT / "private-key.pem", "rb")
        self.private_key = load_pem_private_key(key_file.read(), password=None)
        key_file.close()

        key_file = open(FIXTURES_ROOT / "public-key.pem", "rb")
        self.public_key = key_file.read()
        key_file.close()

    def test_refreshed_access_token_has_kid_in_headers(self):
        jwt_config = settings.SIMPLE_JWT
        jwt_config["ALGORITHM"] = "RS256"
        jwt_config["SIGNING_KEY"] = self.private_key
        jwt_config["VERIFYING_KEY"] = self.public_key
        with override_settings(SIMPLE_JWT=jwt_config):
            refresh_token = ExtendedRefreshToken.for_user(self.user)
        response = self.client.post(
            reverse("token_refresh"), data={"refresh": str(refresh_token)}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        access_token = response.data["access"]
        headers = jwt.get_unverified_header(access_token)
        self.assertIn("kid", headers.keys())


class TokenForServiceTest(TestCase):
    def test_anonymous_access_is_forbidden(self):
        response = self.client.get(
            reverse("token_for_service"),
        )
        self.assertRedirects(
            response,
            f"{reverse('django_cas:login')}?next={reverse('token_for_service')}",
            fetch_redirect_response=False,
        )

    def test_non_superuser_access_forbidden(self):
        user = User.objects.create_user(
            username="username",
            is_active=True,
            is_staff=True,
            is_superuser=False,
        )
        self.client.force_login(user)
        response = self.client.get(
            reverse("token_for_service"),
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_not_found_in_ldap_is_forbidden(self):
        user = User.objects.create_user(
            username="username",
            is_active=True,
            is_staff=True,
            is_superuser=True,
        )
        service = AuthorizedService.objects.create(
            data={"service": "localhost", "fields": {"username": "uid"}},
        )
        self.client.force_login(user)
        with patch("jwtserver.apps.token_api.serializers.get_user") as get_user_mock:
            get_user_mock.side_effect = LDAPUserNotFoundError
            response = self.client.post(
                reverse("token_for_service"),
                data={"service": service.id},
            )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_superadmin_can_access(self):
        user = User.objects.create_user(
            username="username",
            is_active=True,
            is_staff=True,
            is_superuser=True,
        )
        self.client.force_login(user)
        response = self.client.get(
            reverse("token_for_service"),
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
