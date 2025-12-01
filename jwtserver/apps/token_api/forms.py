from django import forms
from django.utils.translation import gettext_lazy as _

from jwtserver.apps.token_api.models import AuthorizedService


class TokenForServiceForm(forms.Form):
    service = forms.ModelChoiceField(
        queryset=AuthorizedService.objects.all(),
        label=_("Select the target service"),
        empty_label=_("-- Select a service --"),
        help_text=_(
            "The token will be generated with your current rights for this specific service."
        ),
        widget=forms.Select(attrs={"aria-labelledby": "id_service_hint"}),
    )
