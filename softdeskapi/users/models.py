from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    """Custom user manager."""

    def create_user(
        self, username, birth_date, can_be_contacted, can_data_be_shared, password=None
    ):
        """
        Creates and saves a User with the given attributes.
        Checks if the user is at least 15 years old.
        """
        if not username:
            raise ValueError("Users must have a username")
        if not birth_date:
            raise ValueError("Users must have a birth date")
        # check if user is at least 15 years old
        if (timezone.now().date() - birth_date).days < 15 * 365:
            raise ValueError("Users must be at least 15 years old (RGPD)")
        user = self.model(
            username=username,
            birth_date=birth_date,
            can_be_contacted=can_be_contacted,
            can_data_be_shared=can_data_be_shared,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, username, birth_date, can_be_contacted, can_data_be_shared, password=None
    ):
        """Same as create_user but with is_staff and is_superuser set to True."""
        user = self.create_user(
            username=username,
            birth_date=birth_date,
            can_be_contacted=can_be_contacted,
            can_data_be_shared=can_data_be_shared,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model. Username is used as the primary identifier.
    Due to RGPD, a user must be over 15 years old to register and he can choose
    if he allows to contact him and if his data can be shared.
    """

    username = models.CharField(max_length=150, unique=True)
    birth_date = models.DateField()
    can_be_contacted = models.BooleanField(default=False)
    can_data_be_shared = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_time = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["birth_date", "can_be_contacted", "can_data_be_shared"]

    def __str__(self):
        return self.username
