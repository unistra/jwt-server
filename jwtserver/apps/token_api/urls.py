from django.conf.urls import url

from jwtserver.apps.token_api.views import TokenObtainCASView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    url(r'^token/(?P<redirect_url>[=\w]+)$', TokenObtainCASView.as_view(), name='token_obtain_cas'),
    url(r'^token/refresh/$', TokenRefreshView.as_view(), name='token_refresh'),
]
