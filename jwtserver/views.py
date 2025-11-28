from django.shortcuts import render
from django.utils.translation import gettext_lazy as _


def home(request):
    return render(
        request,
        'pages/home.html',
        {
            'services': [
                {
                    'title': _('Standard Authentication'),
                    'description': _(
                        'Exchanges a standard CAS ticket for a pair of tokens (Access + Refresh). Automatically retrieves the user\'s LDAP attributes.'
                    ),
                    'icon': 'us us-user',
                    'color': 'oklch(0.55 0.22 262.89)',
                    'is_debug': False,
                    'api': {
                        'path': 'api/token/',
                        'method': 'POST',
                    },
                },
                {
                    'title': _('Session Renewal'),
                    'description': _(
                        'Allows maintaining the user session active without CAS re-authentication by exchanging a valid Refresh Token for a new Access Token.'
                    ),
                    'icon': 'us us-arrows-rotate',
                    'color': 'oklch(0.6 0.13 163.22)',
                    'is_debug': False,
                    'api': {
                        'path': 'api/token/refresh/',
                        'method': 'POST',
                    },
                },
                {
                    'title': _('Token-o-Matic'),
                    'description': _(
                        'Machine-to-Machine authentication system. Allows a backend service to obtain an access token for another service via an ApplicationToken.'
                    ),
                    'icon': 'nv nv-android',
                    'color': 'oklch(0.56 0.25 320.33)',
                    'is_debug': False,
                    'api': {
                        'path': 'api/token-o-matic/',
                        'method': 'POST',
                    },
                },
                {
                    'title': _('Service Verification'),
                    'description': _(
                        'Utility endpoint to verify the validity of a CAS ticket or the accessibility of a registered remote service.'
                    ),
                    'icon': 'us us-arrows-rotate',
                    'color': 'oklch(0.65 0.19 41.11)',
                    'is_debug': False,
                    'api': {
                        'path': 'api/service/verify/',
                        'method': 'POST',
                    },
                },
                {
                    'title': _('Dummy Mode'),
                    'description': _(
                        'Authentication simulator for development environments. Only works with DEBUG=True.'
                    ),
                    'icon': 'us us-flask-sm',
                    'color': 'oklch(0.45 0.18 95.31)',
                    'is_debug': True,
                    'api': {'path': 'api/dummy/token', 'method': 'GET'},
                },
            ]
        },
    )
