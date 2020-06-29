from django.contrib.postgres.fields import JSONField

from django.db import models


class AuthorizedService(models.Model):
    data = JSONField(blank=True, default=dict)
    creation_date = models.DateTimeField(auto_now_add=True)
