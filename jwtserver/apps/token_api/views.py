import base64
from urllib.parse import urlencode

import requests
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenViewBase

from jwtserver.apps.token_api.serializers import TokenObtainCASSerializer


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def redirect_ticket(request, **kwargs):
    custom_headers = {}
    try:
        redirect_url = base64.b64decode(kwargs['redirect_url']).decode("utf-8")
        custom_headers['service'] = request.build_absolute_uri('?')
        custom_headers['ticket'] = request.GET.get('ticket')
    except UnicodeDecodeError as e:
        return Response("Error decoding '{}'".format(kwargs['redirect_url']), status=status.HTTP_400_BAD_REQUEST)

    response = HttpResponse(None, status=status.HTTP_307_TEMPORARY_REDIRECT)
    response['Location'] = redirect_url + '?' + urlencode(custom_headers)
    return response


# def eat_ticket(request, **kwargs):
#     data = {
#         'service': request.GET.get('service'),
#         'ticket': request.GET.get('ticket')}
#     distant = requests.post("http://127.0.0.1:8000/api/token/", data=data)
#     if distant.status_code != 200:
#         return Response("Error consuming ticket : '{}'".format(distant.status_code), status=status.HTTP_400_BAD_REQUEST)
#
#     return HttpResponse(distant.text, status=status.HTTP_200_OK, content_type='application/json')


class TokenObtainCASView(TokenViewBase):
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.
    """
    serializer_class = TokenObtainCASSerializer

    def post(self, request, *args, **kwargs):
        service = request.POST.get('service')
        ticket = request.POST.get('ticket')
        serializer = self.get_serializer(data={**request.data, **{'ticket': ticket, 'service': service}})

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK, )


token_obtain_pair = TokenObtainCASView.as_view()
