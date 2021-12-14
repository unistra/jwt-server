import json
from functools import lru_cache
from uuid import NAMESPACE_DNS, uuid3

import jwt
from cryptography.hazmat.primitives.hashes import SHA256
from django.conf import settings
from jwt.algorithms import RSAPSSAlgorithm
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken, Token


def force_https(uri):
    if settings.STAGE not in ('dev',) and uri[:5] != 'https':
        uri = uri.replace('http://', 'https://')
    return uri


@lru_cache()
def generate_jwks():
    key_id = generate_public_key_id()
    data = json.loads(RSAPSSAlgorithm(SHA256).to_jwk(_public_key()))
    data['kid'] = key_id
    return {'keys': [data]}


@lru_cache()
def generate_public_key_id():
    return str(uuid3(NAMESPACE_DNS, str(_public_key().public_numbers().e)))


def _public_key():
    private_key = settings.SIMPLE_JWT['SIGNING_KEY']
    return private_key.public_key()


class ExtendedToken(Token):
    def __str__(self):
        return jwt.encode(
            self.payload,
            key=settings.SIMPLE_JWT['SIGNING_KEY'],
            algorithm="RS256",
            headers={"kid": generate_public_key_id()},
        )


class ExtendedRefreshToken(RefreshToken, ExtendedToken):
    def __str__(self):
        return ExtendedToken.__str__(self)

    @property
    def access_token(self):
        access = ExtendedAccessToken()
        access.set_exp(from_time=self.current_time)

        no_copy = self.no_copy_claims
        for claim, value in self.payload.items():
            if claim in no_copy:
                continue
            access[claim] = value

        return access


class ExtendedAccessToken(AccessToken, ExtendedToken):
    def __str__(self):
        return ExtendedToken.__str__(self)
