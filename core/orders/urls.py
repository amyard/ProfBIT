from django.urls import path
from core.orders.views import OrdersCreateView, OrderByDateView


app_name='orders'

urlpatterns = [
    path('', OrdersCreateView.as_view(), name='base_view'),
    path('order-by-date/', OrderByDateView.as_view(), name='order_by_date'),
]