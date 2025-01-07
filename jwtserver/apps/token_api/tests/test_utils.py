import base64

from django.test import TestCase
from django.urls import reverse

from jwtserver.apps.token_api.utils import decode_service


class DecodeServiceTest(TestCase):
    def test_decode_service(self):
        encoded = f"https://jwtserver.unistra.fr{reverse('redirect_ticket', kwargs={'redirect_url': base64.urlsafe_b64encode(b'https://authorized_service.unistra.fr').decode()})}"
        self.assertEqual(
            decode_service(encoded),
            "authorized_service.unistra.fr",
        )

    def test_decode_service_with_port(self):
        encoded = f"https://jwtserver.unistra.fr{reverse('redirect_ticket', kwargs={'redirect_url': base64.urlsafe_b64encode(b'https://authorized_service.unistra.fr:8080').decode()})}"
        self.assertEqual(
            decode_service(encoded),
            "authorized_service.unistra.fr",
        )

    def test_decode_service_with_query_params(self):
        encoded = f"https://jwtserver.unistra.fr{reverse('redirect_ticket', kwargs={'redirect_url': base64.urlsafe_b64encode(b'https://authorized_service.unistra.fr/path?param1=value1&param2=value2').decode()})}"
        self.assertEqual(
            decode_service(encoded),
            "authorized_service.unistra.fr",
        )

    def test_decode_service_fails(self):
        encoded = f"https://jwtserver.unistra.fr{reverse('redirect_ticket', kwargs={'redirect_url': base64.urlsafe_b64encode(b'this_is_not_an_expected_url_format').decode()})}"
        self.assertEqual(
            decode_service(encoded),
            "",
        )
