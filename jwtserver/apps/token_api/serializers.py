import sentry_sdk
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django_cas.backends import CASBackend
from rest_framework import serializers
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken

from jwtserver.apps.token_api.models import AdditionalUserInfo
from jwtserver.libs.api.client import get_user


class UserTokenSerializer(serializers.Serializer, ):
    """
    Token serializer
    """
    def validate_user(self, attrs, user):
        data = super().validate(attrs)
        refresh = self.get_token(user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        return data


class TokenObtainCASSerializer(UserTokenSerializer):
    """
    Generates token in exchange of a CAS ticket
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ticket'] = serializers.CharField()
        self.fields['service'] = serializers.CharField()

    def get_token(self, user):
        t = RefreshToken.for_user(user)
        t['iss'] = self.context['request'].get_host()
        try:
            self.verifyUserData(user)
            t['directory_id'] = user.additionaluserinfo.directory_id
        except ObjectDoesNotExist:
            # No additional information exists. Already covered by validation
            pass
        return t

    def validate(self, attrs):
        d = CASBackend().authenticate(ticket=attrs['ticket'], service=attrs['service'])
        if not d:
            raise AuthenticationFailed()
        self.verifyUserData(d)
        return self.validate_user(attrs, d)

    def verifyUserData(self, user):
        """
        Verifies if a user has additional data. If not, it will try to get it from the information system
        :param user: user to check
        :return: None
        """
        try:
            user.additionaluserinfo.directory_id
        except ObjectDoesNotExist:
            response = get_user(username=user.username)
            if len(response.data['results']) > 0:
                c_user = response.data['results'][0]
                if 'accounts' in c_user:
                    for account in c_user['accounts']:
                        if account['username'] == user.username:
                            directory_id = account['directory_id']
                            print(directory_id)
                            goc = AdditionalUserInfo.objects.get_or_create(user=user)
                            if goc[1]:
                                goc[0].directory_id = directory_id
                                goc[0].save()
            else:
                sentry_sdk.capture_message("No Camelot result for username {}".format(user.username))


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
        return RefreshToken.for_user(User(username='dummy'))

    def validate(self, attrs):
        return self.validate_user(attrs, User(username='dummy'))


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for users
    """

    class Meta:
        model = User
        fields = ('id', 'username',)
