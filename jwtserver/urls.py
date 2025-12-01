from django.conf import settings
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import include, path, re_path
from django_cas.views import login as cas_login

from .apps.token_api.views import jwks
from .views import home

admin.autodiscover()

cas_base = settings.CAS_SERVER_URL.rstrip('/')
cas_logout_url = f"{cas_base}/logout"

urlpatterns = [
    # Examples:
    path('', home, name="home"),
    path('api/', include("jwtserver.apps.token_api.urls")),
    path("accounts/", include("django_cas.urls")),
    path('admin/', admin.site.urls),
    re_path(r"^.well-known/jwks.json", jwks, name='jwks'),
    path('login/', cas_login, name='login'),
    path('logout/', LogoutView.as_view(next_page=cas_logout_url), name='logout'),
]

# debug toolbar for dev
if settings.DEBUG and "debug_toolbar" in settings.INSTALLED_APPS:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
