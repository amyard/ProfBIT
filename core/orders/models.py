from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.common.utils import random_date

import random

class Order(models.Model):
    number = models.PositiveIntegerField(_('Number'), blank=True, default='')
    created_date = models.DateTimeField(_('Created Date'), default=random_date, blank=True)

    def __str__(self):
        return f'{self.number}'

    class Meta:
        ordering = ['-pk']

    def save(self, *args, **kwargs):
        try:
            self.number = Order.objects.all().values('pk')[0]['pk']+1
        except:
            self.number = 1
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
        self.product_name = f'Товар-{random.randint(1, 50)}'
        self.product_price = random.randint(100, 9999)
        self.amount = random.randint(1, 10)
        super(OrderItem, self).save(*args, **kwargs)