from django.contrib import admin
from core.orders.models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'number', 'created_date',)