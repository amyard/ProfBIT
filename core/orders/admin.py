from django.contrib import admin
from core.orders.models import Order, OrderItem, QueueToDBModel


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'number', 'created_date',)



@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'product_name', 'product_price', 'amount', )
    search_fields = ['product_name']
    list_filter = ['product_name']


@admin.register(QueueToDBModel)
class QueueToDBModelAdmin(admin.ModelAdmin):
    list_display = ('ip', 'product_by_date', 'top_hundred', 'created')
    list_filter = ['product_by_date', 'top_hundred']