# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-11-25 15:43
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('token_api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='additionaluserinfo',
            name='user',
        ),
        migrations.DeleteModel(
            name='AdditionalUserInfo',
        ),
    ]
