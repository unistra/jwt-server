from django.conf import settings
from django.urls import path, re_path

from . import views

urlpatterns = [
    path(
        'token/',
        views.TokenObtainCASView.as_view(),
        name="token_obtain_cas",
    ),
    path('token/refresh/', views.TokenRefreshView.as_view(), name="token_refresh"),
    path('service/', views.service, name="token_service"),
    path('service/verify', views.service_verify, name="token_service_verify"),
    re_path(
        r"^redirect/(?P<redirect_url>[=\w]+)$",
        views.redirect_ticket,
        name="redirect_ticket",
    ),
    path(
        'token-o-matic/',
        views.TokenOMaticView.as_view(),
        name="token_o_matic",
    ),
]

if settings.DEBUG:
    urlpatterns.extend(
        [
            path(
                'dummy/token',
                views.TokenObtainDummyView.as_view(),
                name="dummy_token",
            ),
            path(
                'dummy/verify',
                views.DummyList.as_view(),
                name="dummy_verify",
            ),
        ]
    )
