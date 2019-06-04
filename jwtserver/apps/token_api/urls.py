from django.conf.urls import url

from jwtserver.apps.token_api.views import TokenObtainCASView, redirect_ticket#, eat_ticket
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    url(r'^token/$', TokenObtainCASView.as_view(), name='token_obtain_cas'),
    url(r'^token/refresh/$', TokenRefreshView.as_view(), name='token_refresh'),
    url(r'^redirect/(?P<redirect_url>[=\w]+)$', redirect_ticket, name='redirect_ticket'),
    # url(r'^miam/$', eat_ticket, name='eat_ticket'),
]
