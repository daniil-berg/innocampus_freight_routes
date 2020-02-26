"""My boilerplate custom user model"""
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class CustomUser(PermissionsMixin, AbstractBaseUser):
    # Fields inherited from AbstractBaseUser:
    # password = ...
    # last_login = ...

    # Fields inherited from PermissionsMixin:
    # is_superuser = ...
    # groups = ...
    # user_permissions = ...

    # Custom(-ized) fields:
    email = models.EmailField(
        verbose_name=_('Email address'),
        max_length=255,
        unique=True,
    )
    is_staff = models.BooleanField(
        verbose_name=_('Staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        verbose_name=_('Account active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(
        verbose_name=_('Date of registration'),
        default=timezone.now
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        return super().has_perm(perm=perm, obj=obj)

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        return super().has_module_perms(app_label=app_label)
