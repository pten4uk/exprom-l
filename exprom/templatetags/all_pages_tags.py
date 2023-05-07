from django import template

from apps.catalog.models import Category
from apps.telegram.forms import OrderForm

register = template.Library()


@register.simple_tag()
def get_categories():
    return Category.objects.all()


@register.simple_tag()
def get_order_form():
    return OrderForm()
