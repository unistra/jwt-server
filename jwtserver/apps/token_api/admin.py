from django.contrib import admin

from .models import (AuthorizedService, )


@admin.register(AuthorizedService)
class AuthorizedServiceAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'keys')

    def keys(self, obj):
        if 'fields' in obj.data:
            return ', '.join(obj.data['fields'].keys())
        return ''
