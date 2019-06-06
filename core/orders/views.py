from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.views.generic import View
from django.utils import timezone

from core.orders.forms import GenerateOrderForm, OrderByDateForm
from core.orders.models import Order, OrderItem
from core.common.script import get_orders_by_date, get_top_hundred_product
from core.common.utils import clean_date_for_orderbydateview

from random import randint
import pandas as pd



class OrdersCreateView(View):
    template_name='orders/main.html'
    form=GenerateOrderForm
    model=Order
    message_send = 'Success: Orders and OrderItems were created.'

    def get(self, request, *args, **kwargs):
        context = {'form':self.form}
        return render(self.request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST or None)
        if form.is_valid():

            numb = form.cleaned_data['number']
            for i in range(1, numb+1):
                md = self.model.objects.create()
                for i in range(1, randint(2,6)):
                    OrderItem.objects.create(order_id = md)
            messages.success(self.request, self.message_send)
            return HttpResponseRedirect('/')
        context = {'form': self.form(request.POST or None)}
        return render(self.request, self.template_name, context)




class OrderByDateView(View):
    template_name = 'orders/order_by_date.html'
    form = OrderByDateForm
    model = Order

    def get(self, request, *args, **kwargs):
        context = {'form': self.form}
        return render(self.request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST or None)
        if form.is_valid():
            start_date = form.cleaned_data['start_period']
            end_date = form.cleaned_data['end_date']

            # fix warning
            start = clean_date_for_orderbydateview(start_date)
            end = clean_date_for_orderbydateview(end_date)

            df = pd.DataFrame(list(OrderItem.objects.filter(order_id__created_date__range=[start, end]).order_by('-order_id__created_date').values('order_id__created_date','order_id', 'product_name','product_price','amount')))
            df_result = get_orders_by_date(df)

            context={'form':self.form, 'df_result':df_result}
            return render(self.request, self.template_name, context)
        context = {'form': self.form(request.POST or None)}
        return render(self.request, self.template_name, context)



class TopHundredView(View):
    template_name = 'orders/top_100.html'
    model = Order

    def get(self, request, *args, **kwargs):
        df = pd.DataFrame(list(OrderItem.objects.all().order_by('-order_id__created_date').values('order_id__created_date', 'order_id', 'product_name', 'product_price','amount')))
        df_result = get_top_hundred_product(df)

        context={'df_result':df_result}
        return render(self.request, self.template_name, context)
