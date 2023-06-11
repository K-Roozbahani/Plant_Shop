from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from django.views import View
from django.http import HttpRequest, Http404

from .api.views import ProductApiView, CartApiView, CartItemApiView
from .models import Product, CartItem
from .utils.views.apis import get_cart


class ProductView(View):
    def get(self, request, pk=None):
        cart = get_cart(request)
        if not pk:
            api_products = ProductApiView.as_view({'get': 'list'})(request)
            if api_products.status_code != 200:
                return Http404()
            context = {'products': api_products.data, 'cart': cart}
            return render(request, 'shop-fullwidth.html', context)
        elif pk:
            top_products = Product.valid_objects.all().order_by("priority")[:6]
            api_product = ProductApiView.as_view({'get': 'retrieve'})(request=request, pk=pk)
            if api_product.status_code != 200:
                HttpResponse(status=404, content="product not found")
            context = {'product': api_product.data, 'cart': cart, 'top_products': top_products}
            return render(request, 'product-details.html', context)


class CartView(View):
    def get(self, request, pk=None):
        cart = get_cart(request)
        if not pk:
            context = {'cart': cart}
            return render(request, 'cart.html', context)
        elif pk:
            updated_card = CartItemApiView.as_view({'get': "destroy"})(request=request, pk=pk)
            if updated_card.status_code not in [200, 204]:
                print("status code: \t", updated_card.status_code)
                print("status_text: \t", updated_card.status_text)
                print("context_data: \t", updated_card.context_data)
                print("data: \t", updated_card.data)
                raise Http404()

            return HttpResponseRedirect("/products/cart/")

    def post(self, request, pk=None):

        # if pk not none add one new item

        if pk is not None:
            new_item = CartItemApiView.as_view({'post': 'create'})(request=request)
            if new_item.status_code in [200, 201]:
                return HttpResponseRedirect("/products/cart/")
            else:
                print("status code: \t", new_item.status_code)
                print("status_text: \t", new_item.status_text)
                print("context_data: \t", new_item.context_data)
                print("data: \t", new_item.data)
                raise Http404()

        if pk is None:
            cart_items = CartItem.valid_objects.filter(cart__user=request.user).select_related("product")
            request_cart_items = []
            products = list(request.POST.keys())
            for product_id in products[1:]:
                try:
                    item = cart_items.get(product__id=int(product_id))
                except CartItem.DoesNotExist:
                    continue
                if item.count != int(request.POST.get(product_id)):
                    item.count = int(request.POST.get(product_id))
                    request_cart_items.append(item)
            CartItem.objects.bulk_update(request_cart_items, ["count"])
            return HttpResponseRedirect("/products/cart/")
