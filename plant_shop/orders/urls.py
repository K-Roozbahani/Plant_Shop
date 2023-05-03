from django.urls import path

from .views import CheckoutView

urlpatterns = [
    path("", CheckoutView.as_view(), name="checkout"),
    path("/<int:pk>", CheckoutView.as_view(), name="checkout_retrieve"),
]
