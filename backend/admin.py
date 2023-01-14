from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from backend.models import User, ConfirmEmailToken

# admin.site.register(User)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Панель управления пользователями
    """
    model = User

    fieldsets = (
        (None, {'fields': ('email', 'password', 'type')}),
        ('Personal info', {'fields': ('_name', )}),
        ('Permissions', {
            'fields': ('is_active', 'is_superuser',  'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ('email', '_name')



# @admin.register(Contact)
# class ContactAdmin(admin.ModelAdmin):
#     pass


@admin.register(ConfirmEmailToken)
class ConfirmEmailTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'key', 'created_at',)