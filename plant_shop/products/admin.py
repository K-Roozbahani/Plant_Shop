from django.contrib import admin
from .models import Product, Picture, Category, ProductAttribute, CartItem, Cart


class PictureTabularInline(admin.TabularInline):
    model = Picture
    fields = ('owner', 'image', "number")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    model = Category


@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    model = ProductAttribute


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    model = Product
    inlines = [PictureTabularInline]


class CartItemTabularInLine(admin.TabularInline):
    model = CartItem
    Fields = ["product", "count", "is_valid", "updated_time"]
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    model = Cart
    inlines = [CartItemTabularInLine]
