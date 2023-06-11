from rest_framework import serializers

from ..models import Category, ProductAttribute, Product, Cart, CartItem, Picture


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


class PictureSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = Picture
        fields = ("id", "image", "number")


class ProductSerializer(serializers.ModelSerializer):
    attributes = ProductsAttributeSerializer(many=True)
    categories = serializers.StringRelatedField(many=True)
    image = serializers.ImageField(use_url=True)
    pictures = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'categories', 'name', 'price', 'stock', 'description', 'attributes', 'image', 'pictures')

    def get_pictures(self, obj):
        try:
            pictures = obj.pictures.all().order_by("number")
        except:
            return None
        return PictureSerializer(instance=pictures, many=True, read_only=True).data


# this class get product primary key and display product data serializer
class ProductRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        serializer = ProductSerializer(value)
        product = {"id": serializer.data["id"], "name": serializer.data['name'],
                   "price": serializer.data['price'], "image": serializer.data["image"]}
        return product

    def to_internal_value(self, data):
        if type(data) == str and data.isnumeric():
            data = int(data)
        if type(data) != int:
            raise serializers.ValidationError(f"Input must be integer not {type(data)}")
        try:
            product_instance = Product.valid_objects.get(id=data)
        except Product.DoesExist:
            raise serializers.ValidationError("Products dose not exist")
        return product_instance


class CartItemSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()
    product = ProductRelatedField(queryset=Product.valid_objects.all())

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'count', 'total_price']

    def create(self, validated_data):
        user = self.context['request'].user
        cart = Cart.objects.get(user=user)
        try:
            instance = CartItem.valid_objects.get(product=validated_data["product"], cart=cart)
        except CartItem.DoesNotExist:
            instance = CartItem.objects.create(cart=cart, **validated_data)
            return instance
        instance.count = validated_data["count"]
        instance.save()
        return instance

    def get_total_price(self, obj):
        return obj.get_price()


class CartItemsRelatedField(serializers.RelatedField):
    def to_representation(self, value=None):
        if value is None:
            return None

        else:
            cart_items = value.filter(is_valid=True)
            return CartItemSerializer(instance=cart_items, many=True).data

    def to_internal_value(self, data):
        pass


class CartSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    cart_items = CartItemsRelatedField(read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'total_price', 'discount', 'cart_items']
