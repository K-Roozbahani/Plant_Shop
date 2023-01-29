from django.db import models
from django.utils.translation import gettext_lazy as _


class ValidManager(models.Manager):
    def get_queryset(self):
        return super(ValidManager, self).get_queryset().filter(is_valid=True)


class AbstractModel(models.Model):
    is_valid = models.BooleanField(verbose_name=_('is valid'), default=True)
    created_time = models.DateTimeField(verbose_name=_('created time'), auto_now_add=True)
    updated_time = models.DateTimeField(verbose_name=_('updated time'), auto_now=True)

    objects = models.Manager()
    valid_objects = ValidManager()

    class Meta:
        abstract = True
