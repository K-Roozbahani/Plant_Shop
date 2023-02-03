from django.shortcuts import render
from .api.views import ProductApiView


def product_view(request, pk=None):
    if not pk:
        api_response = ProductApiView.as_view({'get': 'list'})(request).data
        print(api_response)
        products = [dict(product) for product in api_response]
        print(products)
        context = {'products': products}
        return render(request, 'products.html', context)
    elif pk:
        if not pk:
            api_response = ProductApiView.as_view({'get': 'retrieve'})(request).data
            print(api_response)
            productc = dict(api_response)
            print(productc)
            context = {'products': productc}
            return render(request, 'products.html', context)
