from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from django.views import View

from .api.views import ProductApiView, CartApiView, CartItemApiView
from .models import Product


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
            top_products = Product.valid_objects.all().order_by("priority")[:6]
            api_product = ProductApiView.as_view({'get': 'retrieve'})(request=request, pk=pk)
            if api_product.status_code != 200:
                HttpResponse(status=404, content="product not found")
            context = {'product': api_product.data, 'cart': cart.data, 'top_products': top_products}
            return render(request, 'product-details.html', context)


class CartView(View):
    def get(self, request, pk=None):
        cart = CartApiView.as_view({'get': 'list'})(request)
        if cart.status_code != 200:
            HttpResponse(status=404, content="somthing wrong happen")

        if not pk:
            for item in cart.data["cart_items"]:
                print('kaveh    :-------', item["product"]["name"])
            context = {'cart': cart.data}
            return render(request, 'cart.html', context)
        elif pk:
            updated_card = CartItemApiView.as_view({'get': "destroy"})(request=request, pk=pk)
            print(updated_card.status_code)
            if updated_card.status_code != 200:
                HttpResponse(status=404, content="Somthing wrong happen")
            return HttpResponseRedirect("/products/cart/")
