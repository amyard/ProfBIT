from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.common.utils import get_random_date

import random

class Order(models.Model):
    number = models.PositiveIntegerField(_('Number'), blank=True, default='')
    created_date = models.DateTimeField(_('Created Date'), default=get_random_date(1), blank=True)

    def __str__(self):
        return f'{self.number}'

    class Meta:
        ordering = ['-pk']

    def save(self, *args, **kwargs):
        try:
            ids = Order.objects.all().values('pk')[0]['pk']+1
            self.number = ids
            self.created_date = get_random_date(ids)
        except:
            self.number = 1
            self.created_date = get_random_date(1)
        super(Order, self).save(*args, **kwargs)



class OrderItem(models.Model):
    order_id=models.ForeignKey(Order, on_delete = models.CASCADE, related_name='orders')
    product_name=models.CharField(_('Product'), max_length=55, blank=True)
    product_price=models.PositiveIntegerField(_('Price'), blank=True)
    amount=models.PositiveIntegerField(_('Amount'), blank=True)

    def __str__(self):
        return f'{self.order_id.number}-{self.product_name}'

    class Meta:
        ordering = ['-pk']

    def save(self, *args, **kwargs):
        self.product_name = f'Товар-{random.randint(1, 200)}'
        self.product_price = random.randint(100, 9999)
        self.amount = random.randint(1, 10)
        super(OrderItem, self).save(*args, **kwargs)

    def full_price(self):
        return self.product_price*self.amount