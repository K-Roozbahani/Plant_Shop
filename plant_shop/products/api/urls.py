from rest_framework.routers import DefaultRouter
from .views import ProductApiView, CategoryApiView

router = DefaultRouter()
router.register(r'product', ProductApiView, 'api-products')
router.register(r'categories', CategoryApiView, 'api-categories')
urlpatterns = router.urls
