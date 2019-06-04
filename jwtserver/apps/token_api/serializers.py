from django.contrib.auth.models import User
from django_cas.backends import CASBackend, verify_proxy_ticket
from rest_framework import serializers
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken


class TokenObtainCASSerializer(serializers.Serializer):
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
        user = User.objects.get(username__iexact=d)
        data = super().validate(attrs)
        refresh = self.get_token(user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        return data
