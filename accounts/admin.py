from django.contrib import admin
from .models import Account
from django.contrib.auth.admin import UserAdmin
# Register your models here.


class AccountAdmin(UserAdmin):
    list_display = ('email', 'name', 'username',
                    'last_login', 'date_joined', 'is_admin')
    list_display_links = ('email', 'name')
    readonly_fields = ('last_login', 'date_joined')
    ordering = ['-date_joined']

    filter_horizontal = ()
    filter_vertical = ()
    fieldsets = ()


admin.site.register(Account, AccountAdmin)
