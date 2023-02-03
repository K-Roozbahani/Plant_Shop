from rest_framework import serializers

from ..models import Category, ProductAttribute, Product


class ProductsAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttribute
        fields = ('id', 'title', 'value', 'description', 'sub_attribute')
        depth = 1


class ProductSerializer(serializers.ModelSerializer):
    attributes = ProductsAttributeSerializer(many=True)
    categories = serializers.StringRelatedField(many=True)
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = Product
        fields = ('id', 'categories', 'name', 'price', 'stock', 'categories', 'attributes', 'image')