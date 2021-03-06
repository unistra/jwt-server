# Generated by Django 2.2.17 on 2021-03-23 13:37

from django.db import migrations, models
import django.db.models.deletion
import jwtserver.apps.token_api.models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('token_api', '0003_authorizedservice'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApplicationToken',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('account', models.CharField(help_text='LDAP account to generate a token for', max_length=255, null=True)),
                ('auth_token', models.CharField(default=jwtserver.apps.token_api.models.generate_auth_token, max_length=255)),
                ('authorized_service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='token_api.AuthorizedService')),
            ],
        ),
    ]
