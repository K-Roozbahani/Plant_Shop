from django.shortcuts import render
from .api.views import ProductApiView


def product_view(request, pk=None):
    if not pk:
        api_products = ProductApiView.as_view({'get': 'list'})(request).data
        context = {'products': api_products}
        return render(request, 'products.html', context)
    elif pk:
        if not pk:
            api_product = ProductApiView.as_view({'get': 'retrieve'})(request).data
            context = {'products': api_product}
            return render(request, 'products.html', context)
