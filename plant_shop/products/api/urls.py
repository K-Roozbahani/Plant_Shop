from rest_framework.routers import DefaultRouter
from .views import ProductApiView, CategoryApiView, CartApiView, CartItemApiView

router = DefaultRouter()
router.register(r'products', ProductApiView, 'api-products')
router.register(r'categories', CategoryApiView, 'api-categories')
router.register(r'cart', CartApiView, 'api-cart')
router.register(r'cart/items', CartItemApiView, 'api-cart-items')
urlpatterns = router.urls
