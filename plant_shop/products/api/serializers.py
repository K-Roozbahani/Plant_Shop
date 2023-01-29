from rest_framework import serializers

from ..models import Category, ProductAttribute, Product


class ProductsAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttribute
        field = ('id', 'title', 'value', 'description', 'sub_attribute')
        depth = 1


class ProductSerializer(serializers.ModelSerializer):
    attributes = ProductsAttributeSerializer
    categories = serializers.StringRelatedField(many=True)

    class Meta:
        model = Product
        field = ('categories', 'name', 'price', 'stock', 'categories', 'attributes')
