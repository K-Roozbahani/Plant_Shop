from rest_framework import viewsets
from rest_framework import mixins
from ..models import Product, Category
from .serializers import ProductSerializer, CategorySerializer


class ProductApiView(viewsets.ReadOnlyModelViewSet):
    queryset = Product.valid_objects.all()
    serializer_class = ProductSerializer


class CategoryApiView(viewsets.ReadOnlyModelViewSet):
    queryset = Category.valid_objects.perifetch_related('sub_categories').all()
    serializer_class = CategorySerializer
