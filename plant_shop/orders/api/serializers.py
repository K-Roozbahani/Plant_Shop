from rest_framework import serializers
from ..models import Order, OrderItem, DeliveryInformation, Checkout


class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'user', 'status', 'tracking_code', 'orders_price', 'payment_type', 'is_paid')

    def create(self, validated_data):
        user = self.context['request'].user
        instance = Order.Create(user=user, **validated_data)
        return instance


class OrderDetailSerializer(serializers.models):
    user = serializers.StringRelatedField()
    status = serializers.SerializerMethodField()
    payment_type = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ('id', 'user', 'status', 'tracking_code', 'orders_price', 'payment_type', 'is_paid')

    def get_status(self, obj):
        return obj.get_status_display()

    def get_payment_type(self, obj):
        return obj.get_payment_type()

    def create(self, validated_data):
        user = self.context['request'].user
        instance = Order.Create(user=user, **validated_data)
        return instance


class OrderItemSerializer(serializers.ModelSerializer):
    order = OrderDetailSerializer(write_only=True)
    price = serializers.SerializerMethodField()

    # product = ProductSerializer()

    class Meta:
        model = OrderItem()
        fields = ['order', 'product', 'expire_time', 'count', 'price', 'created_time', 'modified_time']

    def get_price(self, obj):
        return obj.get_price()

    # def validate_order(self, value):

    def validate(self, data):
        if data['count'] > data['product'].stock:
            raise serializers.ValidationError('product is not exist')
        return super(OrderItemSerializer, self).validate(data)


class DeliveryInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryInformation
        fields = ('id', 'user', 'first_name', 'last_name', 'phone_number', 'address', 'postal_code')


class CheckoutSerializer(serializers.ModelSerializer):
    delivery_information = DeliveryInformationSerializer()

    class Meta:
        model = Checkout
        fields = ('id', 'delivery_information', 'order', 'post_type', 'send_cost', 'tracking_code')

