from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *

class UserAdmin(BaseUserAdmin):
    # Add 'is_professional' to the fieldsets so it appears on the user change form
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Professional Info', {'fields': ('is_professional',)}),  # Custom field here
    )

    # Add 'is_professional' to the add_fieldsets so it appears on the user creation form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'is_professional'),  # Custom field here
        }),
    )

admin.site.register(User, UserAdmin)
admin.site.register(Booking)
admin.site.register(Service)
admin.site.register(Review)


admin.site_header = 'Justbookit Administration'

admin.site_title = 'Justbookit site admin'

