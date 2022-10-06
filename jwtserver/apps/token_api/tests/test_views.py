from pathlib import Path

import jwt
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from django.conf import settings
from django.contrib.auth.models import User
from django.test import override_settings
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from jwtserver.apps.token_api.utils import ExtendedRefreshToken

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
