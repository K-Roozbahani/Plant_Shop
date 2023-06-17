from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    message = "Phone number must be entered in the format '+123456789'. Up to 15 digits allowed."

    phone_number = models.CharField(verbose_name=_('phone number'), max_length=16, unique=True,
                                    validators=[RegexValidator(regex=r'^09\d{9}$', message=message)])
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ['first_name', 'last_name']

# regex=r'^\+?1?\d{9,15}$
