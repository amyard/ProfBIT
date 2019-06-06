from django.urls import path
from core.orders.views import OrdersCreateView, OrderByDateView, TopHundredView


app_name='orders'

urlpatterns = [
    path('', OrdersCreateView.as_view(), name='base_view'),
    path('order-by-date/', OrderByDateView.as_view(), name='order_by_date'),
    path('top-100/', TopHundredView.as_view(), name='top_100'),
]