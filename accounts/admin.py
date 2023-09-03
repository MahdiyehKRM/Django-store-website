from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .forms import *
from .models import User, Mobile


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreateForm
    list_display = ('email', 'phone', 'f_name', 'l_name')
    list_filter = ('create', 'is_active')
    fieldsets = (
        ('user', {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('is_admin',)}),
        ('Permissions', {'fields': ('is_active', 'is_superuser')})
    )
    add_fieldsets = (
        (None, {'fields': ('email', 'f_name', 'l_name', 'phone', 'password1', 'password2')}),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
admin.site.register(Mobile)
