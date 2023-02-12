from rest_framework.routers import DefaultRouter
from .views import OrderApiView
router = DefaultRouter()
router.register('order', OrderApiView, 'api-order')
urlpatterns = router.urls
