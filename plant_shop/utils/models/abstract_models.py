from django.db import models
from django.utils.translation import gettext_lazy as _


class AbstractModel(models.Model):
    is_valid = models.BooleanField(verbose_name=_('is valid'), default=True)
    created_time = models.DateTimeField(verbose_name=_('created time'), auto_now_add=True)
    updated_time = models.DateTimeField(verbose_name=_('updated time'), auto_now=True)

    class Meta:
        abstract = True
