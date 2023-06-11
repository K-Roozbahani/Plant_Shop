from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, FormParser
from ..models import Product, Category, Cart, CartItem
from .serializers import (ProductSerializer, CategorySerializer, CartSerializer,
                          CartItemSerializer)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination


class ProductApiView(viewsets.ReadOnlyModelViewSet):
    queryset = Product.valid_objects.prefetch_related("pictures").all().order_by('priority')
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['categories']
    search_fields = ['name', 'categories__title']
    ordering_fields = ['created_time', 'price']
    ordering = ['created_time']
    pagination_class = PageNumberPagination
    page_size = 8
    parser_classes = [JSONParser, FormParser]


class CategoryApiView(viewsets.ReadOnlyModelViewSet):
    queryset = Category.valid_objects.all()
    serializer_class = CategorySerializer
    parser_classes = [JSONParser]


class CartApiView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser]

    def list(self, request):
        cart, is_create = Cart.valid_objects.get_or_create(user=request.user)
        print(cart, is_create)
        total_price = 0
        if not is_create:
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
    serializer_class = CartItemSerializer
    parser_classes = [JSONParser, FormParser]

    def get_queryset(self):
        cart = self.request.user.cart
        return CartItem.valid_objects.filter(cart=cart)
