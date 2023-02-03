from rest_framework import viewsets
from rest_framework import mixins
from ..models import Product
from .serializers import ProductSerializer


class ProductApiView(viewsets.ReadOnlyModelViewSet):
    queryset = Product.valid_objects.all()
    serializer_class = ProductSerializer
