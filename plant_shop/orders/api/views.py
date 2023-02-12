from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import (OrderDetailSerializer, OrderItemSerializer, OrderSerializer,
                          DeliveryInformationSerializer, CheckoutSerializer)
from ..models import OrderItem, Order, DeliveryInformation, Checkout


# ------------ create order ---------------
class OrderApiView(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Order.valid_objects.prefetch_related('order_items').filter(user=user)
