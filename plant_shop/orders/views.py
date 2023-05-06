from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from .forms import DeliveryInformationForm
from .models import DeliveryInformation, Order, OrderItem, Checkout
from products.models import CartItem, Cart
from products.utils.views.apis import get_cart


class CheckoutView(View):
    def post(self, request):
        user = request.user
        cart = get_cart(request)
        # --check delivery information
        try:
            delivery_information = DeliveryInformation.valid_objects.get(DeliveryInformation, user=request)
        except DeliveryInformation.DoesNotExist:
            delivery_information = DeliveryInformation(user=user)

        # --form
        form = DeliveryInformationForm(data=request.post, instance=delivery_information)
        if not form.is_valid():
            return self.get(request=request, form=form)
        elif form.has_changed():
            form.save()

        # --create order
        order = Order.objects.create(user=user)
        delivery_information = form.instance
        order_items = []
        cart_items = CartItem.valid_objects.filter(cart__user=user).select_related("product")
        for item in cart_items:
            order_item = OrderItem(order=order, product=item.product, conut=item.count)
            if order_item.is_available():
                order.orders_price += order_item.get_price()
        order_items = OrderItem.valid_object.bulk_craete(order_items)
        if order_items:
            order.save()
            Checkout.objects.create(delivery_information=delivery_information, order=order)
            return render(request, "checkout.html", context={"cart": cart, "form": form})

    def get(self, request, pk=None, form=None):
        cart = get_cart(request)
        # display forms errors
        if form:
            return render(request, "checkout.html", context={"cart": cart, "form": form})
        # display empty form to get information
        elif not form and not pk:
            if cart.get("cart_items"):
                try:
                    delivery_information = DeliveryInformation.valid_objects.get(user=request.user)
                    form = DeliveryInformationForm(instance=delivery_information)
                except DeliveryInformation.DoesNotExist:
                    form = DeliveryInformationForm()
            else:
                return HttpResponseRedirect("products/cart/")
            return render(request, "checkout.html", context={"cart": cart, "form": form})
        # display order information
        elif pk:
            pass
