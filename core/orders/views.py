from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.views.generic import View

from core.orders.forms import GenerateOrderForm, OrderByDateForm
from core.orders.models import Order, OrderItem

from random import randint




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
            messages.success(self.request, 'Success: AWESOME')
            return HttpResponseRedirect(reverse('orders:order_by_date'))
        context = {'form': self.form(request.POST or None)}
        return render(self.request, self.template_name, context)
