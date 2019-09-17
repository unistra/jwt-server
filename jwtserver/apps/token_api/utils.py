from django.conf import settings


def force_https(uri):
    if settings.STAGE != 'dev' and uri[:5] != 'https':
        uri = uri.replace('http://', 'https://')
    return uri
