from django.shortcuts import render
from .api.views import ProductApiView


def product_view(request, pk=None):
    if not pk:
        api_response = ProductApiView.as_view({'get': 'list'})(request).data
        products = [dict(product) for product in api_response]
        context = {'products': products}
        return render(request, 'products.html', context)
    elif pk:
        if not pk:
            api_response = ProductApiView.as_view({'get': 'retrieve'})(request).data
            product = dict(api_response)
            context = {'products': product}
            return render(request, 'products.html', context)
