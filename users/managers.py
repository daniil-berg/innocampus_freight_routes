"""My boilerplate custom user manager"""
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, email: str, password: str, **other_fields) -> AbstractBaseUser:
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError(_("Users must have an email address"))

        user = self.model(
            email=self.normalize_email(email),
            # Possibly additional fields here...
            **other_fields  # May contain e.g. is_superuser=True or is_active=False
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, password: str, **other_fields):
        """
        Creates and saves a superuser with the given email and password.
        """
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)

        if other_fields['is_staff'] is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if other_fields['is_superuser'] is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        user = self.create_user(
            email=email,
            password=password,
            # Possibly additional fields here...
            **other_fields
        )
        user.save(using=self._db)
        return user
