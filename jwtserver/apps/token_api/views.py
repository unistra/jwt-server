import base64

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


class TokenObtainCASView(TokenViewBase):
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.
    """
    serializer_class = TokenObtainCASSerializer

    def get(self, request, *args, **kwargs):
        redirect_url = base64.b64decode(kwargs['redirect_url']).decode("utf-8")
        service = request.build_absolute_uri('?')
        ticket = request.GET.get('ticket')
        serializer = self.get_serializer(data={**request.data, **{'ticket': ticket, 'service': service}})

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_302_FOUND, headers={'Location': redirect_url,
                    **{'X-Redirect-' + key: value for (key, value) in serializer.validated_data.items()}})


token_obtain_pair = TokenObtainCASView.as_view()

