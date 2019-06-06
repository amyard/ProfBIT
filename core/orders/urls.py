from django.urls import path
from core.orders.views import OrdersCreateView


app_name='orders'

urlpatterns = [
    path('', OrdersCreateView.as_view(), name='base_view'),
]