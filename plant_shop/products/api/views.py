from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models import Product, Category, Cart, CartItem
from .serializers import (ProductSerializer, CategorySerializer, CartSerializer,
                          CartItemCreateSerializer, CartItemDetailSerializer)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination


class ProductApiView(viewsets.ReadOnlyModelViewSet):
    queryset = Product.valid_objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['categories']
    search_fields = ['name', 'categories__title']
    ordering_fields = ['created_time', 'price']
    ordering = ['created_time']
    pagination_class = PageNumberPagination
    page_size = 8


class CategoryApiView(viewsets.ReadOnlyModelViewSet):
    queryset = Category.valid_objects.all()
    serializer_class = CategorySerializer


class CartApiView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        cart = get_object_or_404(Cart, user=request.user)
        total_price = 0
        cart_items = CartItem.valid_objects.filter(cart=cart)

        for item in cart_items:
            total_price += item.get_price()
        if cart.total_price != total_price:
            cart.total_price = total_price
            cart.save()

        serializer = CartSerializer(instance=cart)
        return Response(serializer.data)


class CartItemApiView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        cart = self.request.user.cart
        return CartItem.valid_objects.filter(cart=cart)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return CartItemDetailSerializer
        else:
            return CartItemCreateSerializer
