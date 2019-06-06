from django.contrib import admin
from core.orders.models import Order, OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'number', 'created_date',)



@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'product_name', 'product_price', 'amount', )
    search_fields = ['product_name']
    list_filter = ['product_name']
