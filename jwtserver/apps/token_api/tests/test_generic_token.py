import base64
from urllib.parse import quote_plus
from uuid import uuid4

from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.status import HTTP_302_FOUND

from jwtserver.apps.token_api.models import AuthorizedService


class GenericTokenTests(TestCase):
    def setUp(self):
        TestCase.setUp(self)
        self.username = "dummy"
        self.password = f"{uuid4()}"
        self.user = User.objects.create_user(
            username=self.username, password=self.password
        )
        settings.STAGE = "test"
        AuthorizedService.objects.create(
            data={"service": "authorized_service.unistra.fr"}
        )

    def test_redirect(self):
        target = base64.b64encode(b"http://authorized_service.unistra.fr")
        additional_args = "?ticket=ST-ticket"
        action = reverse("redirect_ticket", kwargs={"redirect_url": target.decode()})
        response = self.client.get(action + additional_args)
        self.assertEqual(response.status_code, HTTP_302_FOUND)
        self.assertEqual(
            response["location"],
            "http://authorized_service.unistra.fr?service={}&ticket=ST-ticket".format(
                quote_plus(
                    "https://testserver/api/redirect/" + str(target.decode("utf-8"))
                )
            ),
        )

    def test_redirect_ticket_invalid_service(self):
        # Create an invalid service URL
        service_url = "https://unauthorized.unistra.fr"
        encoded_service_url = base64.urlsafe_b64encode(service_url.encode()).decode(
            "utf-8"
        )
        # Create a valid ticket
        ticket = "ST-ticket"

        # Make a GET request to the redirect_ticket view
        response = self.client.get(
            reverse("redirect_ticket", kwargs={"redirect_url": encoded_service_url})
            + f"?ticket={ticket}"
        )

        # Assert that the response is a 403 Forbidden
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_redirect_ticket_invalid_redirect_url(self):
        # Create an invalid redirect URL
        redirect_url = base64.urlsafe_b64encode(b"pouic").decode("utf-8")
        # Create a valid ticket
        ticket = "ST-ticket"

        # Make a GET request to the redirect_ticket view
        response = self.client.get(
            reverse("redirect_ticket", kwargs={"redirect_url": redirect_url})
            + f"?ticket={ticket}"
        )

        # Assert that the response is a 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
