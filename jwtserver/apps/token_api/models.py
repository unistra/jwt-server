import secrets
import uuid
from urllib.parse import urlparse

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import JSONField
from django.utils.translation import gettext_lazy as _

from jwtserver.apps.token_api.validators import JSONSchemaValidator


class AuthorizedService(models.Model):
    data = JSONField(
        blank=True,
        default=dict,
        validators=[
            JSONSchemaValidator("authorized_service.schema.json"),
        ],
    )
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if "service" in self.data:
            return self.data["service"]
        return super().__str__()

    def clean(self):
        if (
            self.pk is None
            and AuthorizedService.objects.filter(
                data__service=self.data.get("service")
            ).exists()
        ):
            raise ValidationError(
                {
                    "data": _(
                        "Service \"%(name)s\" already exists"
                        % {"name": self.data.get("service")}
                    )
                }
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    @staticmethod
    def is_valid(url):
        """
        Extracts domain name from URL and checks if it is in the list of authorized services.

        Args:
            url (str): The URL to check.

        Returns:
            bool: True if the domain name is in the list of authorized services, False otherwise.
        """
        # Extract domain name from URL
        domain_name = urlparse(url).hostname

        # Check if domain name is in authorized services
        return AuthorizedService.objects.filter(data__service=domain_name).exists()


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
        help_text=_("LDAP account to generate a token for"),
    )
    auth_token = models.CharField(
        max_length=255, null=False, default=generate_auth_token
    )

    def __str__(self):
        return f'{self.authorized_service.data["service"]} / {self.account}'
