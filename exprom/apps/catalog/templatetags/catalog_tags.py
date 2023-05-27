from django import template
from django.core.paginator import Paginator, Page

from apps.catalog.models import Category, Product

register = template.Library()


@register.inclusion_tag('catalog/include_tags/model_card.html', name='catalog_model_card_tag')
def get_model_card(model: Product, card_class: str = None):
    if card_class is None:
        card_class = 'col col-sm-12 col-md-12 col-lg-3 col-xl-3'

    return {'model': model, "card_class": card_class}


@register.inclusion_tag('catalog/include_tags/pagination.html', name='catalog_pagination_tag')
def get_pagination(paginator: Paginator, page_obj: Page):
    return {'paginator': paginator, 'page_obj': page_obj}
