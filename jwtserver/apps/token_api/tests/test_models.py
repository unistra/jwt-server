from django.test import TestCase

from ..models import ApplicationToken, AuthorizedService


class ApplicationTokenTest(TestCase):

    def test_text_representation(self):
        service = AuthorizedService.objects.create(
            data={"service": "authorized_service.unistra.fr"}
        )
        auth_token = ApplicationToken.objects.create(
            account="login",
            authorized_service=service
        )
        self.assertEqual(
            str(auth_token),
            f"{service.data['service']} / {auth_token.account}"
        )
