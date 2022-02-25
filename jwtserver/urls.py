from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path

from .apps.token_api.views import jwks
from .views import home

admin.autodiscover()

urlpatterns = [
    # Examples:
    path('', home, name="home"),
    path('api/', include("jwtserver.apps.token_api.urls")),
    path("accounts/", include("django_cas.urls")),
    path('admin/', admin.site.urls),
    re_path(r"^.well-known/jwks.json", jwks),
]

# debug toolbar for dev
if settings.DEBUG and "debug_toolbar" in settings.INSTALLED_APPS:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
