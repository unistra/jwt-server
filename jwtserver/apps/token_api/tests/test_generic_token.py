import base64
from urllib.parse import quote_plus
from uuid import uuid4

from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.status import HTTP_302_FOUND


class GenericTokenTests(TestCase):
    def setUp(self):
        TestCase.setUp(self)
        self.username = "dummy"
        self.password = f"{uuid4()}"
        self.user = User.objects.create_user(
            username=self.username, password=self.password
        )
        settings.STAGE = "test"

    def test_redirect(self):
        target = base64.b64encode(b"http://127.0.0.1")
        additional_args = "?ticket=ST-ticket"
        action = reverse("redirect_ticket", kwargs={"redirect_url": target.decode()})
        response = self.client.get(action + additional_args)
        self.assertEqual(response.status_code, HTTP_302_FOUND)
        self.assertEqual(
            response["location"],
            "http://127.0.0.1?service={}&ticket=ST-ticket".format(
                quote_plus(
                    "https://testserver/api/redirect/" + str(target.decode("utf-8"))
                )
            ),
        )
