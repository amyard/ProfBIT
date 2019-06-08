from django import template
from ..models import QueueToDBModel


register = template.Library()

@register.simple_tag
def all_queue():
    return QueueToDBModel.objects.all().count()

@register.simple_tag
def queue_pr_for_date():
    return QueueToDBModel.objects.filter(product_by_date=1).count()

@register.simple_tag
def queue_top_hundred():
    return QueueToDBModel.objects.filter(top_hundred=1).count()