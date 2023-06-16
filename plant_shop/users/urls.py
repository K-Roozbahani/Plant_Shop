from django.urls import path, include

from .views import LoginUser

urlpatterns = [
    path('login/', LoginUser.as_view(), name='login'),
]
