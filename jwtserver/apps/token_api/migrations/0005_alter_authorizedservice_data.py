# Generated by Django 3.2.16 on 2022-10-06 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('token_api', '0004_applicationtoken'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authorizedservice',
            name='data',
            field=models.JSONField(blank=True, default=dict),
        ),
    ]