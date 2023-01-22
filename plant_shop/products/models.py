from django.db import models
from django.utils.translation import gettext_lazy as _

from .utils.models.abstract_models import AbstractModel


class Category(AbstractModel):
    parent_category = models.ForeignKey("Category", on_delete=models.CASCADE, related_name="sub_category",
                                        verbose_name=_('parent category'), null=True, blank=True)
    title = models.CharField(verbose_name=_('title'), max_length=64)

    class Meta:
        db_table = 'category'
        verbose_name = _('category')
        verbose_name_plural = _('category')


class ProductAttribute(AbstractModel):
    title = models.CharField(verbose_name=_('title'), max_length=64)
    description = models.CharField(verbose_name=_('description'), max_length=256, blank=True, null=True)
    value = models.FloatField(verbose_name=_('value'), blank=True, null=True)
    sub_attribute = models.ManyToManyField('ProductAttribute', related_name='parent_attribute',
                                           verbose_name=_('sub_attribute'))

    class Meta:
        db_table = 'product_attribute'
        verbose_name = _('product attribute')
        verbose_name_plural = _('product attributes')


class Product(AbstractModel):
    name = models.CharField(verbose_name=_('name'), max_length=64)
    price = models.PositiveSmallIntegerField(verbose_name=_('price'), default=0)
    stock = models.PositiveSmallIntegerField(verbose_name=_('stock'), default=0)

    class Meta:
        db_table = 'product'
        verbose_name = _('product')
        verbose_name_plural = _('products')
