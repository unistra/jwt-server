import json

from django.contrib import admin
from django.contrib.postgres.forms.jsonb import (
    InvalidJSONInput,
    JSONField as JSONFormField,
)
from django import forms

from .models import (
    ApplicationToken,
    AuthorizedService,
)


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


@admin.register(ApplicationToken)
class ApplicationTokenAdmin(admin.ModelAdmin):
    pass
