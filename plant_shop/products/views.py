from django.shortcuts import render
from .api.views import ProductApiView, CartApiView


def product_view(request, pk=None):
    cart = CartApiView.as_view({'get': 'list'})(request).data
    print(cart)
    if not pk:
        api_products = ProductApiView.as_view({'get': 'list'})(request).data
        context = {'products': api_products, 'cart': cart}
        return render(request, 'shop.html', context)
    elif pk:
        if not pk:
            api_product = ProductApiView.as_view({'get': 'retrieve'})(request).data
            context = {'product': api_product, 'cart': cart}
            return render(request, 'shop.html', context)
