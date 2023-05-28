from django.http import Http404

from ...api.views import CartApiView


def get_cart(request):
    if not request.user.is_authenticated:
        return None
    cart = CartApiView.as_view({'get': 'list'})(request)
    if cart.status_code != 200:
        raise Http404("user need to log")
    return cart.data