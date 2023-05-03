from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.views import View
from .forms import DeliveryInformationForm
from .models import DeliveryInformation, Order, OrderItem, Checkout
from plant_shop.products.models import CartItem


class CheckoutView(View):

    @login_required
    def post(self, request):
        user = request.user
        # --check delivery information
        try:
            delivery_information = DeliveryInformation.valid_objects.get(DeliveryInformation, user=request)
        except DeliveryInformation.DoesNotExist:
            delivery_information = DeliveryInformation(user=user)

        # --form
        form = DeliveryInformationForm(data=request.post, instance=delivery_information)
        if not form.is_valid():
            return Http404()
        else:
            return self.get(request, form)
        if form.has_changed():
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
            checkout = Checkout.objects.create(delivery_information=delivery_information, order=order)
        return render("")

    @login_required
    def get(self, request, pk=None, form=None):

        # display forms errors
        if form:
            return render(request, "checkout.html", context={"form": form})
        # display empty form to get information
        elif not form and not pk:
            try:
                delivery_information = DeliveryInformation.valid_objects.get(DeliveryInformation, user=request)
                form = DeliveryInformationForm(instance=delivery_information)
            except DeliveryInformation.DoesNotExist:
                form = DeliveryInformationForm()
            return render(request, "checkout.html", context={"form": form})
        # display order information
        elif pk:
            pass
