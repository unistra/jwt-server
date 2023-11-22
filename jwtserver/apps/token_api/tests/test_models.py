from django.core.exceptions import ValidationError
from django.test import TestCase

from ..models import ApplicationToken, AuthorizedService


class ApplicationTokenTest(TestCase):
    def test_text_representation(self):
        service = AuthorizedService.objects.create(
            data={"service": "authorized_service.unistra.fr"}
        )
        auth_token = ApplicationToken.objects.create(
            account="login", authorized_service=service
        )
        self.assertEqual(
            str(auth_token), f"{service.data['service']} / {auth_token.account}"
        )

    def test_authorized_service_name_must_be_unique(self):
        data = {"service": "authorized_service.unistra.fr"}
        AuthorizedService.objects.create(data=data)
        with self.assertRaises(ValidationError) as ctx:
            AuthorizedService.objects.create(data=data)
        self.assertEqual(
            'Service "authorized_service.unistra.fr" already exists',
            ctx.exception.message_dict["data"][0],
        )

    def test_invalid_json_for_authorized_service_raises_validation_error(self):
        data = {
            "service": "authorized_service.unistra.fr",
            "unexpected": "field",
        }
        with self.assertRaises(ValidationError) as ctx:
            AuthorizedService.objects.create(data=data)
        self.assertIn(
            "JSON Schema validation error",
            ctx.exception.message_dict["data"][0],
        )
        self.assertIn(
            "Additional properties are not allowed",
            ctx.exception.message_dict["data"][0],
        )
