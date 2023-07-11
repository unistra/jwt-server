import json

from django import forms
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.forms import JSONField as JSONFormField
from django.forms.fields import InvalidJSONInput
from django.utils.translation import gettext_lazy as _

from .models import ApplicationToken, AuthorizedService


class PrettyJSONField(JSONFormField):
    # https://code.djangoproject.com/ticket/29150
    # https://code.djangoproject.com/ticket/26482

    def prepare_value(self, value):
        if isinstance(value, InvalidJSONInput):
            return value
        return json.dumps(value, indent=4)


class AuthorizedServiceForm(forms.ModelForm):
    class Meta:
        field_classes = {"data": PrettyJSONField}
        widgets = {"data": forms.Textarea(attrs={"rows": 20, "cols": 80})}


@admin.register(AuthorizedService)
class AuthorizedServiceAdmin(admin.ModelAdmin):
    form = AuthorizedServiceForm
    list_display = ("__str__", "keys")

    def keys(self, obj):
        if "fields" in obj.data:
            return ", ".join(obj.data["fields"].keys())
        return ""


class ApplicationTokenForm(forms.ModelForm):
    class Meta:
        model = ApplicationToken
        fields = "__all__"

    def clean_account(self):
        account = self.cleaned_data.get("account")
        User = get_user_model()
        try:
            User.objects.get(username=account)
        except User.DoesNotExist:
            raise forms.ValidationError(
                _("User %(account)s does not exist"),
                params={"account": account},
                code="invalid",
            )
        return account


@admin.register(ApplicationToken)
class ApplicationTokenAdmin(admin.ModelAdmin):
    readonly_fields = ["auth_token"]
    form = ApplicationTokenForm
