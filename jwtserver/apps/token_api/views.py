import base64
from urllib.parse import urlencode

from django.contrib.auth.models import User
from django.http import HttpResponse
from rest_framework import status, permissions
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenViewBase

from jwtserver.apps.token_api.serializers import TokenObtainCASSerializer, TokenObtainDummySerializer, UserSerializer


def get_tokens_for_user(user):
    """
    Generates pair of tokens for user
    :param user: authenticated user
    :return: dict of tokens
    """
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


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
        redirect_url = base64.b64decode(kwargs['redirect_url']).decode("utf-8")
        uri = request.build_absolute_uri('?')
        if uri[:5] != 'https':
            uri = uri.replace('http://', 'https://')
        custom_headers['service'] = uri
        custom_headers['ticket'] = request.GET.get('ticket')
    except UnicodeDecodeError as e:
        return Response("Error decoding '{}'".format(kwargs['redirect_url']), status=status.HTTP_400_BAD_REQUEST)

    response = HttpResponse(None, status=status.HTTP_302_FOUND)
    response['Location'] = redirect_url + '?' + urlencode(custom_headers)
    return response


class DummyList(ListCreateAPIView):
    """
    List of users
    """
    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        return super().get_queryset().filter(username__iexact=self.request.user.username)


class TokenObtainCASView(TokenViewBase):
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.
    """
    serializer_class = TokenObtainCASSerializer

    def post(self, request, *args, **kwargs):
        service = request.data.get('service')
        ticket = request.data.get('ticket')
        serializer = self.get_serializer(data={**request.data, **{'ticket': ticket, 'service': service}})
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK, )


class TokenObtainDummyView(TokenViewBase):
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.
    """
    serializer_class = TokenObtainDummySerializer

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(data={**request.data, **{'dummy': 'dummy', }})

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK, )
