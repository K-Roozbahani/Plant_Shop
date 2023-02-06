from rest_framework import serializers

from ..models import Category, ProductAttribute, Product, Cart, CartItem


class CategorySerializer(serializers.ModelSerializer):
    parent_category = serializers.StringRelatedField()

    class Meta:
        model = Category
        fields = ('id', 'title', 'parent_category')


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


class CartItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'count']

    def create(self, validated_data):
        user = self.context['request'].user
        cart = Cart.objects.get(user=user)
        instance = CartItem.objects.create(cart=cart, **validated_data)
        return instance


class CartSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'total_price', 'discount']


class CartItemDetailSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()
    product = ProductSerializer()

    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'product', 'count', 'price']

    def get_price(self, obj):
        return obj.product.price * obj.count
