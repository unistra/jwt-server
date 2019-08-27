from django.contrib.auth.models import User
from django.db import models


class AdditionalUserInfo(models.Model):
    user = models.OneToOneField(User)
    directory_id = models.CharField(max_length=30)
