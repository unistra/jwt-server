from django import forms

from jwtserver.apps.token_api.models import AuthorizedService


class TokenForServiceForm(forms.Form):
    service = forms.ModelChoiceField(queryset=AuthorizedService.objects.all())
    token = forms.CharField(required=False, widget=forms.Textarea)
