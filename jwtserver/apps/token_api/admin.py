from django.contrib import admin

from .models import (AuthorizedService,)

@admin.register(AuthorizedService)
class AuthorizedServiceAdmin(admin.ModelAdmin):
    pass
