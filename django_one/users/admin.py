from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

User = get_user_model()


@admin.register(User)
class UserAdmin(UserAdmin):
    pass
    fieldsets = [
        (
            None,
            {
                'fields': ('username', 'password')
            }
        ),

        (
            'Персональная информация',
            {
                'fields': ('first_name', 'last_name', 'email')
            }
        ),
        (
            'Права доступа',
            {
                'fields':
                    ('is_active', 'email_verify', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
            }
         ),
        (
            'Важные даты',
            {
                'fields':
                    ('last_login', 'date_joined')
            }
        )
    ]
    readonly_fields = ('last_login', 'date_joined',)
    list_display = ('email', 'is_superuser', 'email_verify', 'date_joined',)
