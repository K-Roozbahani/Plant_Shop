from rest_framework import serializers
from ..models import Order, OrderItem, DeliveryInformation, Checkout
from products.api.serializers import ProductSerializer, ProductRelatedField
from products.models import Product


class OrderItemSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()
    order = serializers.PrimaryKeyRelatedField(queryset=Order.valid_objects.all(), allow_empty=True)
    product = ProductRelatedField(queryset=Product.valid_objects.all())

    class Meta:
        model = OrderItem
        fields = ['order', 'product', 'expire_time', 'count', 'price']

    def get_price(self, obj):
        return obj.get_price()

    def validate(self, data):
        if data['count'] > data['product'].stock:
            raise serializers.ValidationError('product is not exist')
        return super(OrderItemSerializer, self).validate(data)


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'is_open', 'user', 'get_status_display', 'orders_price',
                  'get_payment_type_display', 'is_paid', 'order_items', 'status', 'payment_type')
        read_only_fields = ('orders_price', 'is_paid')
        extra_kwargs = {'status': {'write_only': True, 'default': 1},
                        'payment_type': {'write_only': True, 'default': 1}}

    def create(self, validated_data):
        order_items_data = validated_data.pop('order_items')
        user = self.context['request'].user
        if not order_items_data:
            return serializers.ValidationError('order_items can not empty')
        order = Order.objects.create(user=user, **validated_data)
        for order_item_data in order_items_data:
            order_item = OrderItem.objects.create(order=order, **order_item_data)
            order.order_items.add(order_item)
            order.orders_price += order_item.get_price()
        order.save()
        return order

    def update(self, instance, validated_data):
        items_instance = instance.order_items.all()
        items_data = validated_data.pop("order_items")
        price = 0
        for item_data in items_data:
            item_id = item_data.get("id")
            item_count = item_data.get("count")
            new_items = []
            edited_items = []

            # If order item is exits update it else create new order itme

            # --------------------------------------------------> edite order item
            if item_id:
                try:
                    item_instance = items_instance.get(id=item_id)
                except:
                    raise serializers.ValidationError("Order Item dose not exist")
                item_instance.count = item_count
                if item_instance.is_available():
                    # item_instance.save() ------------------------------->save
                    edited_items.append(item_instance)
                    price += item_instance.get_price()
                else:
                    raise serializers.ValidationError("This number of product is not available in stock")

            # --------------------------------------------------> crete new order item
            elif not item_id:
                item_instance = OrderItem(order=instance, **item_data)
                if item_instance.is_available():
                    new_items.append(item_instance)
                    price += item_instance.get_price()
                else:
                    raise serializers.ValidationError("This number of product is not available in stock")


class DeliveryInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryInformation
        fields = ('id', 'user', 'first_name', 'last_name', 'phone_number', 'address', 'postal_code')


class CheckoutSerializer(serializers.ModelSerializer):
    delivery_information = DeliveryInformationSerializer()
    order = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Checkout
        fields = ('id', 'order', 'delivery_information', 'order', 'post_type', 'send_cost', 'tracking_code')
