import secrets
import uuid

from django.contrib.postgres.fields import JSONField
from django.db import models


class AuthorizedService(models.Model):
    data = JSONField(blank=True, default=dict)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if "service" in self.data:
            return self.data["service"]
        return super().__str__()


def generate_auth_token():
    return secrets.token_urlsafe(50)


class ApplicationToken(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    authorized_service = models.ForeignKey(
        AuthorizedService,
        on_delete=models.CASCADE,
        related_name="applications",
    )
    account = models.CharField(
        max_length=255,
        null=True,
        help_text="LDAP account to generate a token for",
    )
    auth_token = models.CharField(
        max_length=255, null=False, default=generate_auth_token
    )

    def __str__(self):
        return f'{self.authorized_service.data["service"]} / {self.account}'
