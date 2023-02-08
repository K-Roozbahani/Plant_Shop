from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.conf import settings
from products.models import Product, CartItem
from products.utils.models.abstract_models import AbstractModel


class Order(AbstractModel):
    STATUS_WAIT_FOR_PAYMENT = 1
    STATUS_PREPARING_TO_SEND = 2
    STATUS_SEND_SHIPMENT = 3
    STATUS_DELIVERED_SHIPMENT = 4
    STATUS_RETURNED = 5
    STATUS_CANCEL = 6
    ORDER_STATUS = ((STATUS_WAIT_FOR_PAYMENT, _('wait for payment')),
                    (STATUS_PREPARING_TO_SEND, _('preparing to send')),
                    (STATUS_SEND_SHIPMENT, _('send shipment')),
                    (STATUS_DELIVERED_SHIPMENT, _('delivered shipment')),
                    (STATUS_CANCEL, _('cancel')))

    PAYMENT_ONLINE = 1
    PAYMENT_CASH = 2
    PAYMENT_TYPE = ((PAYMENT_ONLINE, _('online')), (PAYMENT_CASH, _('cash')))

    # -----------------fields-----------------------
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, related_name='orders', verbose_name='user')
    status = models.PositiveIntegerField(verbose_name=_('status'), default=1, choices=ORDER_STATUS)
    tracking_code = models.BigAutoField(verbose_name=_('tracking code'))
    orders_price = models.PositiveBigIntegerField(verbose_name=_('order price'), default=0)
    payment_type = models.PositiveSmallIntegerField(verbose_name=_('payment type'), choices=PAYMENT_TYPE, default=1)
    is_paid = models.BooleanField(verbose_name=_('is paid'), default=False)

    class Meta:
        db_table = 'order'
        verbose_name = 'order'
        verbose_name_plural = 'orders'


class OrderItem(AbstractModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="order_items")
    expire_time = models.DateTimeField(default=timezone.now() + timezone.timedelta(hours=1))
    count = models.PositiveSmallIntegerField(default=0)

    class Meta:
        db_table = 'order_item'
        verbose_name = 'order item'
        verbose_name_plural = 'order items'

    def get_price(self):
        return self.product.price * self.count

    def is_available(self):
        product = self.product
        if product.stock < self.count:
            return False
        return True


class DeliveryInformation(AbstractModel):
    user = models.ForeignKey(settings.AUT_USER_MODEL, models.CASCADE,
                             related_name='delivery_information', verbose_name='user')
    first_name = models.CharField(verbose_name=_('first name'), max_length=64)
    last_name = models.CharField(verbose_name=_('last name'), max_length=64)
    phone_number = models.PositiveBigIntegerField(verbose_name=_('phone number'),
                                                  validators=[RegexValidator(
                                                      r'^989[0-3,9]\d{8}$', 'Enter a valid phone number.',
                                                      'invalid')]
                                                  )
    address = models.TextField(verbose_name=_('address'))
    postal_code = models.PositiveIntegerField(verbose_name=_('postal code'),
                                              validators=[MaxValueValidator(9_999_999_999),
                                                          MinValueValidator(1_000_000_000)])

    class Meta:
        unique_together = ('address', 'phone_number')
        db_table = 'delivery_information'
        verbose_name = 'delivery information'
        verbose_name_plural = 'deliveries information'


class CheckOut(AbstractModel):
    NORMAL_POST = 1
    FAST_POST = 2
    POST_TYPE = ((NORMAL_POST, _('normal')), (FAST_POST, _('fast')))
    delivery_information = models.ForeignKey(DeliveryInformation, models.CASCADE,
                                             related_name='checkouts', verbose_name=_('delivery information'))
    order = models.OneToOneField(Order, models.CASCADE, related_name='order_send')
    post_type = models.PositiveSmallIntegerField(verbose_name=_('post type'), default=1, choices=POST_TYPE)
    send_cost = models.PositiveBigIntegerField(verbose_name=_('send cost'), default=0)
    created_time = models.DateTimeField(verbose_name=_('created time'), auto_now_add=True)
    modified_time = models.DateTimeField(verbose_name=_('modified time'), auto_now=True)
    tracking_code = models.PositiveIntegerField(verbose_name=_('tracking code'), auto_created=True, unique=True)

    class Meta:
        db_table = 'checkout'
        verbose_name = 'checkout'
        verbose_name_plural = 'checkout'
