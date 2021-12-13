import base64
import json
from urllib.parse import urlencode
from uuid import NAMESPACE_DNS, uuid3

import requests
from cryptography.hazmat.primitives._serialization import PublicFormat
from cryptography.hazmat.primitives.hashes import SHA256
from django.conf import settings
from django.contrib.auth.models import User
from django.http import Http404, HttpResponse, JsonResponse
from django.urls import reverse
from jwt import PyJWK
from jwt.algorithms import RSAPSSAlgorithm
from rest_framework import permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenViewBase
from sentry_sdk import add_breadcrumb, capture_message

from ...libs.api.client import UserNotFoundError
from .models import ApplicationToken, AuthorizedService
from .serializers import (
    ApplicationTokenSerializer,
    TokenObtainCASSerializer,
    TokenObtainDummySerializer,
    UserSerializer,
)
from .utils import force_https


def get_tokens_for_user(user):
    """
    Generates pair of tokens for user
    :param user: authenticated user
    :return: dict of tokens
    """
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


def service(request, **kwargs):
    """
    Verification method. Redirects to CAS with GET arguments for validation
    :param request:
    :param kwargs:
    :return:
    """
    verify_url = request.build_absolute_uri(reverse("token_service_verify"))
    service_url = request.build_absolute_uri(
        reverse(
            "redirect_ticket",
            kwargs={
                "redirect_url": base64.urlsafe_b64encode(
                    verify_url.encode()
                ).decode("utf-8")
            },
        )
    )
    cas_url = (
        settings.CAS_SERVER_URL
        + "login?"
        + urlencode({"service": force_https(service_url)})
    )
    response = HttpResponse(None, status=status.HTTP_302_FOUND)
    response["Location"] = cas_url
    return response


def service_verify(request, **kwargs):
    """
    Verification method. Uses ticket to obtain JWS
    :param request:
    :param kwargs:
    :return:
    """
    data = {
        "service": request.GET.get("service"),
        "ticket": request.GET.get("ticket"),
    }
    url = force_https(request.build_absolute_uri(reverse("token_obtain_cas")))
    add_breadcrumb(
        category="auth",
        message=f"url : {url}",
        level="info",
    )
    add_breadcrumb(
        category="auth",
        message=f"data : {data}",
        level="info",
    )
    distant = requests.post(url, data=data)
    if distant.status_code == 200:
        return JsonResponse(
            json.loads(distant.text), status=status.HTTP_200_OK
        )
    if distant.status_code != 401:
        add_breadcrumb(
            category="auth",
            message=f"response code : {distant.status_code}",
            level="info",
        )
        capture_message("Error consuming ticket")
    return JsonResponse(
        {
            "error": "Error consuming ticket : '{}'".format(
                distant.status_code
            ),
            "response": json.loads(distant.text),
        },
        status=distant.status_code,
    )


def redirect_ticket(request, **kwargs):
    """
    Redirects CAS data (service and ticket) to base64 encoded URI.
    Data is sent in GET request
    :param request: GET request
    :param kwargs: additional parameters
    :return:
    """
    custom_headers = {}
    try:
        redirect_url = base64.urlsafe_b64decode(kwargs["redirect_url"]).decode(
            "utf-8"
        )
        uri = force_https(request.build_absolute_uri("?"))
        custom_headers["service"] = uri
        custom_headers["ticket"] = request.GET.get("ticket")
    except UnicodeDecodeError:
        return Response(
            "Error decoding '{}'".format(kwargs["redirect_url"]),
            status=status.HTTP_400_BAD_REQUEST,
        )

    response = HttpResponse(None, status=status.HTTP_302_FOUND)
    response["Location"] = redirect_url + "?" + urlencode(custom_headers)
    return response


def jwks(request):
    private_key = settings.SIMPLE_JWT['SIGNING_KEY']
    public_key = private_key.public_key()
    key_id = str(uuid3(NAMESPACE_DNS, str(public_key.public_numbers().e)))
    data = json.loads(RSAPSSAlgorithm(SHA256).to_jwk(public_key))
    data['kid'] = key_id
    return JsonResponse({'keys':[data]})

class DummyList(ListCreateAPIView):
    """
    List of users
    """

    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(username__iexact=self.request.user.username)
        )


class TokenObtainCASView(TokenViewBase):
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.
    """

    serializer_class = TokenObtainCASSerializer

    def post(self, request, *args, **kwargs):
        service = request.data.get("service")
        ticket = request.data.get("ticket")
        serializer = self.get_serializer(
            data={**request.data, **{"ticket": ticket, "service": service}},
            context={"request": request},
        )
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        except AuthorizedService.DoesNotExist:
            raise PermissionDenied(
                "Unauthorized service, please contact administrators to register your service"  # noqa: E501
            )
        except UserNotFoundError as e:
            return self.permission_denied(request, e)

        return Response(
            serializer.validated_data,
            status=status.HTTP_200_OK,
        )


class TokenOMaticView(TokenViewBase):
    allowed_methods = ["post"]
    queryset = ApplicationToken.objects.all()
    serializer_class = ApplicationTokenSerializer

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service = None
        self.application_token = None

    def post(self, request, *args, **kwargs):
        token = request.data.get("token", None)
        service_name = request.data.get("service", None)
        try:
            self.application_token = self.queryset.get(auth_token=token)
        except ApplicationToken.DoesNotExist:
            return self.permission_denied(request, "invalid_token")
        try:
            self.service = AuthorizedService.objects.get(
                data__service=service_name
            )
        except AuthorizedService.DoesNotExist:
            return self.permission_denied(request, "invalid_service")
        if self.application_token.authorized_service != self.service:
            return self.permission_denied(request, "invalid_token")

        serializer = self.get_serializer(data={**request.data})
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        except (User.DoesNotExist, UserNotFoundError):
            raise Http404
        data = serializer.validated_data
        # We don't want to give refresh tokens
        del data["refresh"]
        return Response(data, status=status.HTTP_200_OK)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["username"] = self.application_token.account
        context["service"] = self.service
        return context


class TokenObtainDummyView(TokenViewBase):
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.
    """

    serializer_class = TokenObtainDummySerializer

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data={
                **request.data,
                **{
                    "dummy": "dummy",
                },
            }
        )

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return JsonResponse(
            serializer.validated_data,
            status=status.HTTP_200_OK,
        )
