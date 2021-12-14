import json
from functools import lru_cache
from uuid import NAMESPACE_DNS, uuid3

from cryptography.hazmat.primitives.hashes import SHA256
from django.conf import settings
from jwt.algorithms import RSAPSSAlgorithm


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
