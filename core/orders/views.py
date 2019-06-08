from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.views.generic import View
from django.utils import timezone

from core.orders.forms import GenerateOrderForm, OrderByDateForm
from core.orders.models import Order, OrderItem, QueueToDBModel
from core.common.script import get_orders_by_date, get_top_hundred_product
from core.common.utils import clean_date_for_orderbydateview, get_random_date, get_ip_from_request


from random import randint
import pandas as pd




class OrdersCreateView(View):
    template_name='orders/main.html'
    form=GenerateOrderForm
    model=Order
    message_send = 'Success: Orders and OrderItems were created.'

    def get(self, request, *args, **kwargs):
        context = {'form':self.form, 'oritem':OrderItem.objects.all(), 'orders':Order.objects.all()}
        return render(self.request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST or None)
        if form.is_valid():

            numb = form.cleaned_data['number']
            orders = Order.objects.bulk_create([ Order(number= Order.objects.all().values('pk')[0]['pk'] + i, created_date = get_random_date(Order.objects.all().values('pk')[0]['pk'] + i)) for i in range(1, numb+1)])
            OrderItem.objects.bulk_create([ OrderItem(order_id=order, product_name=f'Товар-{randint(1, 200)}',
                      product_price=randint(100, 9999), amount=randint(1, 10)) for order in orders for i in range(1, randint(2,6))])
            messages.success(self.request, self.message_send)
            return HttpResponseRedirect('/')
        context = {'form': self.form(request.POST or None), 'oritem':OrderItem.objects.all(), 'orders':Order.objects.all()}
        return render(self.request, self.template_name, context)




class OrderByDateView(View):
    template_name = 'orders/order_by_date.html'
    form = OrderByDateForm
    model = Order

    def get(self, request, *args, **kwargs):
        context = {'form': self.form, 'req_to_db':QueueToDBModel.objects.filter(product_by_date=1).count()}
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

            # number of requests to db
            QueueToDBModel.objects.create(ip=get_ip_from_request(request), product_by_date=1)

            context={'form':self.form, 'df_result':df_result, 'req_to_db':QueueToDBModel.objects.filter(product_by_date=1).count()}
            return render(self.request, self.template_name, context)
        context = {'form': self.form(request.POST or None)}
        return render(self.request, self.template_name, context)



class TopHundredView(View):
    template_name = 'orders/top_100.html'
    model = Order

    def get(self, request, *args, **kwargs):
        df = pd.DataFrame(list(OrderItem.objects.all().order_by('-order_id__created_date').values('order_id__created_date', 'order_id', 'product_name', 'product_price','amount')))
        df_result = get_top_hundred_product(df)

        # number of requests to db
        QueueToDBModel.objects.create(ip=get_ip_from_request(request), top_hundred=1)

        context={'df_result':df_result, 'req_to_db':QueueToDBModel.objects.filter(top_hundred=1).count()}
        return render(self.request, self.template_name, context)
