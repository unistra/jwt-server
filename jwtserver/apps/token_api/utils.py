import base64
import json
import re
from functools import lru_cache
from urllib.parse import urlparse
from uuid import NAMESPACE_DNS, uuid3

import jwt
from cryptography.hazmat.primitives.hashes import SHA256
from django.conf import settings
from jwt.algorithms import RSAPSSAlgorithm
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken, Token


def force_https(uri):
    if settings.STAGE != "dev" and not uri.startswith("https"):
        uri = uri.replace("http://", "https://")
    return uri


def decode_service(encoded_service: str) -> str:
    # base64 decode the service and strip the protocol and port
    try:
        encoded = re.search("/([^/]*)$", encoded_service).group(1)
        decoded_service_and_port = base64.urlsafe_b64decode(encoded).decode("utf-8")
        service = get_domain_from_service(decoded_service_and_port)
    except AttributeError:
        # .group() not an attribute of None (regex does not match)
        return ""
    return service


def get_domain_from_service(service: str) -> str:
    parsed = urlparse(service)
    return parsed.hostname or ""


@lru_cache
def generate_jwks():
    key_id = generate_public_key_id()
    data = json.loads(RSAPSSAlgorithm(SHA256).to_jwk(_public_key()))
    data['kid'] = key_id
    return {'keys': [data]}


@lru_cache
def generate_public_key_id():
    return str(uuid3(NAMESPACE_DNS, str(_public_key().public_numbers().e)))


def _public_key():
    private_key = settings.SIMPLE_JWT['SIGNING_KEY']
    if settings.SIMPLE_JWT['ALGORITHM'] == 'RS256':
        return private_key.public_key()
    else:
        return 'should-define-key-id'


class ExtendedToken(Token):
    def __str__(self):
        headers = (
            {"kid": generate_public_key_id()}
            if settings.SIMPLE_JWT['ALGORITHM'] == 'RS256'
            else None
        )
        return jwt.encode(
            self.payload,
            key=settings.SIMPLE_JWT['SIGNING_KEY'],
            algorithm=settings.SIMPLE_JWT['ALGORITHM'],
            headers=headers,
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
