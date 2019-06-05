from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.common.utils import random_date


class Order(models.Model):
    number = models.PositiveIntegerField(_('Number'), blank=True, default=' ')
    created_date = models.DateTimeField(_('Created Date'), default=random_date, blank=True)

    def __str__(self):
        return f'{self.number} was created {self.created_date}'

    class Meta:
        ordering = ['-pk']

    def save(self, *args, **kwargs):
        self.number = Order.objects.all().count()+1
        super(Order, self).save(*args, **kwargs)