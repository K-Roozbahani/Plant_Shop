from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.validators import MaxValueValidator
from .utils.models.abstract_models import AbstractModel
from users.models import User

from plant_shop import settings


class Category(AbstractModel):
    parent_category = models.ForeignKey("Category", on_delete=models.CASCADE, related_name="sub_categories",
                                        verbose_name=_('parent category'), null=True, blank=True)
    title = models.CharField(verbose_name=_('title'), max_length=64)

    class Meta:
        unique_together = ['parent_category', 'title']
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
                                           verbose_name=_('sub_attribute'), blank=True)

    class Meta:
        db_table = 'product_attribute'
        verbose_name = _('product attribute')
        verbose_name_plural = _('product attributes')

    def __str__(self):
        return self.title


class Product(AbstractModel):

    TOP_PRIORITY = 0
    HIGH_PRIORITY = 1
    NORMAL_PRIORITY = 2
    LOW_PRIORITY = 3
    PRIORITIES = ((TOP_PRIORITY, "top"), (HIGH_PRIORITY, "high"), (NORMAL_PRIORITY, "normal"), (LOW_PRIORITY, "low"))

    image = models.ImageField(verbose_name=_('image'), upload_to='products/images/')
    name = models.CharField(verbose_name=_('name'), max_length=64)
    price = models.PositiveSmallIntegerField(verbose_name=_('price'), default=0)
    stock = models.PositiveSmallIntegerField(verbose_name=_('stock'), default=0)
    categories = models.ManyToManyField(Category, related_name='products', verbose_name=_('categories'))
    attributes = models.ManyToManyField(ProductAttribute, related_name='products', verbose_name=_('attributes'))
    off = models.PositiveIntegerField(verbose_name='off', blank=True, null=True)
    description = models.CharField(verbose_name=_("description"), max_length=1024, blank=True, null=True)
    priority = models.PositiveSmallIntegerField(verbose_name=_("priority"), default=2, choices=PRIORITIES)

    class Meta:
        db_table = 'product'
        verbose_name = _('product')
        verbose_name_plural = _('products')

    def __str__(self):
        return self.name


class Picture(AbstractModel):
    owner = models.ForeignKey(User, models.CASCADE, related_name='pictures', verbose_name=_('owner'))
    image = models.ImageField(verbose_name=_('image'), upload_to='products/pictures/')
    product = models.ForeignKey(Product, models.CASCADE, related_name='pictures', verbose_name=_('product'))
    number = models.PositiveIntegerField(verbose_name=_('number'))

    class Meta:
        unique_together = ("product", "number")
        db_table = 'product_picture'
        verbose_name = _('product picture')
        verbose_name_plural = _('product pictures')

    def __str__(self):
        return f'image {str(self.id)} {self.product.name}'


class ProductChoice(AbstractModel):
    product = models.ForeignKey(Product, models.CASCADE, related_name='Choices', verbose_name=_('product'))
    name = models.CharField(verbose_name=_('name'), max_length=64)
    price = models.PositiveSmallIntegerField(verbose_name=_('price'), default=0)
    stock = models.PositiveSmallIntegerField(verbose_name=_('stock'), default=0)
    default_choice = models.BooleanField(verbose_name='default choice', default=False)
    off = models.PositiveIntegerField(verbose_name='off', blank=True, null=True)

    class Meta:
        unique_together = ['product', 'name']
        db_table = 'product_choice'
        verbose_name = _('product choice')
        verbose_name_plural = _('product choices')


class Cart(AbstractModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                related_name="cart", verbose_name='user')
    is_active = models.BooleanField(verbose_name=_('is active'), default=False)
    total_price = models.PositiveBigIntegerField(verbose_name=_('total price'), default=0)
    discount = models.PositiveBigIntegerField(verbose_name=_('discount'), default=0)

    class Meta:
        db_table = 'cart'
        verbose_name = _('cart')
        verbose_name_plural = _('carts')


class CartItem(AbstractModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items", verbose_name=_('cart'))
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name="cart_items", verbose_name=_('products'))
    expire_time = models.DateTimeField(verbose_name=_('expire time'),
                                       default=timezone.now() + timezone.timedelta(hours=24))
    count = models.PositiveSmallIntegerField(verbose_name=_('count'), default=1)

    def get_price(self):
        return self.product.price * self.count

    def __str__(self):
        return f'{str(self.count)} * {self.product.name}'

    class Meta:
        db_table = 'cart_item'
        verbose_name = _('cart item')
        verbose_name_plural = _('cart items')
