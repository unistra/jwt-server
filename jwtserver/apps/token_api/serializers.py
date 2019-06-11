from django.conf import settings
from django.contrib.auth.models import User
from django_cas.backends import CASBackend
from rest_framework import serializers
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken


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

    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        d = CASBackend().authenticate(ticket=attrs['ticket'], service=attrs['service'])
        if not d:
            raise AuthenticationFailed()
        return self.validate_user(attrs, User.objects.get(username__iexact=d))


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
