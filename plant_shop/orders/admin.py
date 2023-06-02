from django.contrib import admin
from .models import DeliveryInformation, Order, Checkout, OrderItem


class OrderItemTabularInLine(admin.TabularInline):
    model = OrderItem
    fields = ("product", "count", "expire_time")
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    model = Order
    readonly_fields = ["created_time", "updated_time"]
    inlines = [OrderItemTabularInLine]


@admin.register(DeliveryInformation)
class DeliveryInformationAdmin(admin.ModelAdmin):
    model = DeliveryInformation
    readonly_fields = ["created_time", "updated_time"]


@admin.register(Checkout)
class CheckoutAdmin(admin.ModelAdmin):
    model = Checkout
    readonly_fields = ["created_time", "updated_time"]
