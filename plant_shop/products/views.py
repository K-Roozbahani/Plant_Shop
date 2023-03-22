from django.shortcuts import render, redirect, HttpResponse
from django.views import View

from .api.views import ProductApiView, CartApiView


class ProductView(View):
    def get(self, request, pk=None):
        cart = CartApiView.as_view({'get': 'list'})(request)
        if cart.status_code != 200:
            HttpResponse(status=404, content="somthing wrong happen")
        if not pk:
            api_products = ProductApiView.as_view({'get': 'list'})(request)
            if api_products.status_code != 200:
                HttpResponse(status=404, content="somthing wrong happen")
            context = {'products': api_products.data, 'cart': cart.data}
            return render(request, 'shop-fullwidth.html', context)
        elif pk:
            api_product = ProductApiView.as_view({'get': 'retrieve'})(request=request, pk=pk)
            if api_product.status_code != 200:
                HttpResponse(status=404, content="product not found")
            context = {'product': api_product.data, 'cart': cart.data}
            return render(request, 'product-details.html', context)
