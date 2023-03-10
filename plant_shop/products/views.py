from django.shortcuts import render, redirect
from django.views import View

from .api.views import ProductApiView, CartApiView


class ProductView(View):
    def get(self, request, pk=None):
        cart = CartApiView.as_view({'get': 'list'})(request).data
        if not pk:
            api_products = ProductApiView.as_view({'get': 'list'})(request).data
            context = {'products': api_products, 'cart': cart}
            return render(request, 'products_list.html', context)
        elif pk:
            if not pk:
                api_product = ProductApiView.as_view({'get': 'retrieve'})(request).data
                context = {'product': api_product, 'cart': cart}
                return render(request, 'products_list.html', context)
