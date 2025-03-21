import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django_cas.backends import CASBackend
from rest_framework import serializers
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.settings import api_settings

from ...libs.api.client import get_user
from .models import AuthorizedService
from .utils import ExtendedRefreshToken, decode_service

ADDITIONAL_DATA = 'claims'


class UserTokenSerializer(serializers.Serializer):
    """
    Token serializer
    """

    def validate_user(self, attrs, user):
        data = super().validate(attrs)
        refresh = self.get_token(user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        return data

    def get_token(self, user) -> ExtendedRefreshToken:
        token: ExtendedRefreshToken = ExtendedRefreshToken.for_user(user)
        authorized_service = self.get_service()

        token["iss"] = self.get_issuer(authorized_service)
        token["sub"] = user.username
        token["nbf"] = datetime.datetime.now().timestamp()
        additionaluserinfo = self.get_user_info(
            user.username,
            authorized_service.data["fields"],
            conditions=authorized_service.data.get("conditions", None),
        )
        if additionaluserinfo is not None:
            for k, v in additionaluserinfo.items():
                token[k] = v
        if ADDITIONAL_DATA in authorized_service.data:
            for k, v in authorized_service.data[ADDITIONAL_DATA].items():
                token[k] = v
        return token

    def get_issuer(self, authorized_service: AuthorizedService):
        if "issuer" in authorized_service.data:
            return authorized_service.data["issuer"]
        if (
            ADDITIONAL_DATA in authorized_service.data
            and "issuer" in authorized_service.data[ADDITIONAL_DATA]
        ):
            return authorized_service.data[ADDITIONAL_DATA]["issuer"]
        else:
            return self.context["request"].get_host()

    def get_user_info(self, username, fields, conditions=None):
        return get_user(
            username,
            fields,
            conditions=conditions,
        )

    def get_service(self):
        if "request" in self.context and "service" in self.context["request"].POST:
            base = self.context["request"].POST.get("service", False)
        else:
            base = self.context["request"].data.get("service", False)

        service = decode_service(base)
        authorized_service = AuthorizedService.objects.get(data__service=service)

        return authorized_service


class TokenRefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField(read_only=True)

    def validate(self, attrs):
        refresh = ExtendedRefreshToken(attrs["refresh"])

        data = {'access': str(refresh.access_token)}

        if api_settings.ROTATE_REFRESH_TOKENS:
            if api_settings.BLACKLIST_AFTER_ROTATION:
                try:
                    # Attempt to blacklist the given refresh token
                    refresh.blacklist()
                except AttributeError:
                    # If blacklist app not installed, `blacklist` method will
                    # not be present
                    pass

            refresh.set_jti()
            refresh.set_exp()
            refresh.set_iat()

            data['refresh'] = str(refresh)

        return data


class TokenObtainCASSerializer(UserTokenSerializer):
    """
    Generates token in exchange of a CAS ticket
    """

    service = serializers.CharField()
    ticket = serializers.CharField()

    def validate(self, attrs):
        d = CASBackend().authenticate(
            self.context["request"],
            ticket=attrs["ticket"],
            service=attrs["service"],
        )
        if not d:
            raise AuthenticationFailed()
        return self.validate_user(attrs, d)


class ApplicationTokenSerializer(UserTokenSerializer):
    service = serializers.CharField()

    def validate(self, attrs):
        user = User.objects.get(username=self.context["username"])
        return self.validate_user(attrs, user)

    def get_service(self):
        authorized_service = self.context.get("service", None)
        if authorized_service is not None and isinstance(
            authorized_service, AuthorizedService
        ):
            return authorized_service

    def get_user_info(self, username, fields, conditions=None):
        # We want to raise an exception if user is not found in LDAP
        return get_user(
            username,
            fields,
            raise_exception=True,
            conditions=self.context["service"].data.get("conditions", None),
        )


class TokenObtainDummySerializer(UserTokenSerializer):
    """
    Dummy serializer. Only available in debug mode and only for dummy user
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def get_token(cls, user):
        if not settings.DEBUG:
            return None
        token: ExtendedRefreshToken = ExtendedRefreshToken.for_user(user)
        return token

    def validate(self, attrs):
        return self.validate_user(attrs, User(username="dummy"))


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for users
    """

    class Meta:
        model = User
        fields = (
            "id",
            "username",
        )
