from rest_framework import viewsets
from rest_framework import mixins
from ..models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
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
