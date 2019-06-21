from django.conf import settings
from django.conf.urls import url
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from jwtserver.apps.token_api.views import TokenObtainCASView, redirect_ticket, TokenObtainDummyView, DummyList, \
    service, service_verify

urlpatterns = [
    url(r'^token/$', TokenObtainCASView.as_view(), name='token_obtain_cas'),
    url(r'^token/refresh/$', TokenRefreshView.as_view(), name='token_refresh'),
    url(r'^service/$', service, name='token_service'),
    url(r'^service/verify$', service_verify, name='token_service_verify'),
    url(r'^redirect/(?P<redirect_url>[=\w]+)$', redirect_ticket, name='redirect_ticket'),
]

if settings.DEBUG:
    urlpatterns.extend([url(r'^dummy/token$', TokenObtainDummyView.as_view(), name='dummy_token'),
                        url(r'^dummy/verify$', DummyList.as_view(), name='dummy_verify'), ])
