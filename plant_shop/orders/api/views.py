from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import JSONParser

from .serializers import (OrderItemSerializer, OrderSerializer,
                          DeliveryInformationSerializer, CheckoutSerializer)
from ..models import OrderItem, Order, DeliveryInformation, Checkout


# ------------ create order ---------------
class OrderApiView(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser]

    def get_queryset(self):
        user = self.request.user
        return Order.valid_objects.prefetch_related('order_items').filter(user=user)

    @action(methods="get", detail=True, url_path='<int:pk>/checkout/', url_name="checkout_retrieve")
    def checkout_retrieve(self, request, pk=None):
        try:
            checkout = Checkout.valid_objects.prefetch_related("delivery_information", "order").get(order__id=pk)
        except Checkout.DoesNotExist:
            return Response("order not found", status=status.HTTP_404_NOT_FOUND)
        if checkout.order.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = CheckoutSerializer(instance=checkout)
        return Response(serializer.data, status=status.HTTP_200_OK)
