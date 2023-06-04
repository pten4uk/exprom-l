from django import template

from apps.catalog.models import Category
from apps.telegram.forms import OrderForm, QuestionForm

register = template.Library()


@register.simple_tag()
def get_categories():
    return Category.objects.all()


@register.simple_tag()
def get_order_form():
    return OrderForm()


@register.simple_tag()
def get_question_form():
    return QuestionForm()
