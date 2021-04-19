from django.conf import settings
from django.conf.urls import url
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from . import views

urlpatterns = [
    url(
        r"^token/$",
        views.TokenObtainCASView.as_view(),
        name="token_obtain_cas",
    ),
    url(r"^token/refresh/$", TokenRefreshView.as_view(), name="token_refresh"),
    url(r"^service/$", views.service, name="token_service"),
    url(
        r"^service/verify$", views.service_verify, name="token_service_verify"
    ),
    url(
        r"^redirect/(?P<redirect_url>[=\w]+)$",
        views.redirect_ticket,
        name="redirect_ticket",
    ),
    url(
        r"^token-o-matic/",
        views.TokenOMaticView.as_view(),
        name="token_o_matic",
    ),
]

if settings.DEBUG:
    urlpatterns.extend(
        [
            url(
                r"^dummy/token$",
                views.TokenObtainDummyView.as_view(),
                name="dummy_token",
            ),
            url(
                r"^dummy/verify$",
                views.DummyList.as_view(),
                name="dummy_verify",
            ),
        ]
    )
