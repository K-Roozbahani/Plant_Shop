from rest_framework.routers import DefaultRouter
from .views import ProductApiView

router = DefaultRouter()
router.register(r'product', ProductApiView, 'api-products')
urlpatterns = router.urls
