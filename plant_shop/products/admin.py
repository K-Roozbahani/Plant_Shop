from django.contrib import admin
from .models import Product, Picture, Category, ProductAttribute


class PictureTabularInline(admin.TabularInline):
    model = Picture
    fields = ('owner', 'image')


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
