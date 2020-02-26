"""My boilerplate custom user admin"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser
from . forms import CustomUserCreationForm, CustomUserChangeForm


class CustomUserAdmin(UserAdmin):
    """
    Largely copied from https://docs.djangoproject.com/en/3.0/topics/auth/customizing/
    """
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin that reference specific fields on auth.User.
    list_display = ('email', 'is_active', 'is_staff', 'last_login', )
    list_filter = ('is_staff', )
    fieldsets = (
        (None, {
            'fields': ('email', 'password')
        }),
        ('Personal info', {
            'fields': ()
        }),
        ('Permissions', {
            'fields': ('is_staff',)
        }),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    search_fields = ('email', )
    ordering = ('email', )
    filter_horizontal = ()


admin.site.register(CustomUser, CustomUserAdmin)
