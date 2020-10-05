import base64
import datetime
import re

from django.conf import settings
from django.contrib.auth.models import User
from django_cas.backends import CASBackend
from rest_framework import serializers
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken

from jwtserver.apps.token_api.models import AuthorizedService
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

        base = ""
        if 'request' in self.context and 'service' in self.context['request'].POST:
            base = self.context['request'].POST.get('service', False)
        else:
            base = self.context['request'].data.get('service', False)

        encoded = re.search('/([^/]*)$', base).group(1)
        service_and_port = re.search('^https?://([^/]*)?', base64.urlsafe_b64decode(encoded).decode("utf-8")).group(1)
        service = re.search('^([^:]+)(:[0-9]+)?$', service_and_port).group(1)

        # {
        #     "fields": {
        #         "orgUnit": [
        #             "supannEntiteAffectationPrincipale",
        #             "supannEntiteAffectation"
        #         ],
        #         "username": "uid",
        #         "affiliation": [
        #             "eduPersonPrimaryAffiliation",
        #             "eduPersonAffiliation"
        #         ],
        #         "organization": "supannEtablissement"
        #     },
        #     "service": "192.168.0.1"
        # }
        authorized_service = AuthorizedService.objects.get(data__service=service)

        if 'issuer' in authorized_service.data:
            t['iss'] = authorized_service.data['issuer']
        else:
            t['iss'] = self.context['request'].get_host()

        t['sub'] = user.username
        t['nbf'] = datetime.datetime.now().timestamp()
        additionaluserinfo = get_user(user.username, authorized_service.data['fields'])
        if additionaluserinfo is not None:
            for k,v in additionaluserinfo.items():
                t[k] = v
        return t

    def validate(self, attrs):
        d = CASBackend().authenticate(self.context['request'], ticket=attrs['ticket'], service=attrs['service'])
        if not d:
            raise AuthenticationFailed()
        return self.validate_user(attrs, d)



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
