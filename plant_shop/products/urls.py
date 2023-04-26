from django.urls import path
from .views import ProductView, CartView
urlpatterns = [
    path('', ProductView.as_view(), name='products_view'),
    path('<int:pk>/', ProductView.as_view(), name='product_detail'),
    path('cart/', CartView.as_view(), name='cart_items'),
    path('cart/remove/<int:pk>/', CartView.as_view(), name='cart_item_remove')
]
