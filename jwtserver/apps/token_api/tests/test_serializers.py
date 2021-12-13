from unittest.mock import Mock, patch

from django.contrib.auth.models import User
from django.test import RequestFactory, TestCase
from rest_framework.reverse import reverse
from rest_framework_simplejwt.exceptions import AuthenticationFailed

from ..models import AuthorizedService
from ..serializers import TokenObtainCASSerializer, UserTokenSerializer


class UserTokenSerializerTest(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()
        self.service = AuthorizedService.objects.create(
            data={"service": "service_name.unistra.fr"}
        )

    def test_host_name_as_issuer(self):
        request = Mock()
        request.get_host.return_value = "jwtserver.unistra.fr"
        serializer = UserTokenSerializer(data={}, context={"request": request})
        self.assertEqual("jwtserver.unistra.fr", serializer.get_issuer(self.service))

    def test_use_issuer_in_service_if_defined(self):
        service = AuthorizedService.objects.create(
            data={"service": "service_name", "issuer": "issuer.unistra.fr"}
        )
        serializer = UserTokenSerializer(data={}, context={"request": Mock()})
        self.assertEqual("issuer.unistra.fr", serializer.get_issuer(service))

    def test_get_service_from_request(self):
        service = AuthorizedService.objects.create(data={"service": "localhost"})
        request = self.factory.post(
            reverse("token_obtain_cas"),
            {
                "service": "http://jwtserver.unistra.fr:1234/api/redirect/aHR0cDovL2xvY2FsaG9zdDo4MDAxL2FwaS9zZXJ2aWNlL3ZlcmlmeQ==",  # noqa: E501
                "ticket": "ST-712-HJmP7SxCYQmJNCgClgkks60Fc-A-cas6-dev",
            },
        )
        serializer = UserTokenSerializer(data={}, context={"request": request})
        self.assertEqual(service, serializer.get_service())


@patch("jwtserver.apps.token_api.serializers.UserTokenSerializer.validate_user")
@patch("jwtserver.apps.token_api.serializers.CASBackend")
class TokenObtainCASSerializerTest(TestCase):
    def setUp(self) -> None:
        AuthorizedService.objects.create(data={"service": "localhost", "fields": {}})
        self.request = RequestFactory().post(
            reverse("token_obtain_cas"),
            {
                "service": "http://jwtserver.unistra.fr:1234/api/redirect/aHR0cDovL2xvY2FsaG9zdDo4MDAxL2FwaS9zZXJ2aWNlL3ZlcmlmeQ==",  # noqa: E501
                "ticket": "ST-712-HJmP7SxCYQmJNCgClgkks60Fc-A-cas6-dev",
            },
        )
        self.user = User.objects.create_user("username")

    def test_cas_authentication_returns_user(self, cas_mock, serializer_mock):
        cas_mock.return_value.authenticate.return_value = self.user
        serializer_mock.return_value = {
            "service": "service",
            "ticket": "ticket",
            "access": "access",
            "refresh": "refresh",
        }
        serializer = TokenObtainCASSerializer(
            data={}, context={"request": self.request}
        )
        self.assertEqual(
            {
                "service": "service",
                "ticket": "ticket",
                "access": "access",
                "refresh": "refresh",
            },
            serializer.validate({"ticket": "ticket", "service": "service"}),
        )

    def test_cas_authentication_failed_raises_exception(
        self, cas_mock, validate_user_mock
    ):
        cas_mock.return_value.authenticate.return_value = None
        serializer = TokenObtainCASSerializer(
            data={}, context={"request": self.request}
        )
        with self.assertRaises(AuthenticationFailed):
            serializer.validate({"ticket": "ticket", "service": "service"})
