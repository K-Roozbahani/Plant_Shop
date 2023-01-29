from django.db import models
from django.utils.translation import gettext_lazy as _
from .utils.models.abstract_models import AbstractModel
from users.models import User


class Category(AbstractModel):
    parent_category = models.ForeignKey("Category", on_delete=models.CASCADE, related_name="sub_category",
                                        verbose_name=_('parent category'), null=True, blank=True)
    title = models.CharField(verbose_name=_('title'), max_length=64)

    class Meta:
        db_table = 'category'
        verbose_name = _('category')
        verbose_name_plural = _('category')

    def __str__(self):
        return self.title


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

    def __str__(self):
        return self.title


class Product(AbstractModel):
    image = models.ImageField(verbose_name=_('image'), upload_to='products/images/')
    name = models.CharField(verbose_name=_('name'), max_length=64)
    price = models.PositiveSmallIntegerField(verbose_name=_('price'), default=0)
    stock = models.PositiveSmallIntegerField(verbose_name=_('stock'), default=0)
    categories = models.ManyToManyField(Category, related_name='products', verbose_name=_('categories'))
    attributes = models.ManyToManyField(ProductAttribute, related_name='products', verbose_name=_('attributes'))

    class Meta:
        db_table = 'product'
        verbose_name = _('product')
        verbose_name_plural = _('products')

    def __str__(self):
        return self.name


class Picture(AbstractModel):
    owner = models.ForeignKey(User, models.CASCADE, related_name='pictures', verbose_name=_('owner'))
    image = models.ImageField(verbose_name=_('image'), upload_to='products/pictures/')
    product = models.ForeignKey(Product, models.CASCADE, related_name='pictures')

    class Meta:
        db_table = 'product_picture'
        verbose_name = _('product picture')
        verbose_name_plural = _('product pictures')

    def __str__(self):
        return f'image {str(self.id)} {self.product.name}'
