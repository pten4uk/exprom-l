from django.shortcuts import render

from apps.catalog.models import Category, Product


def main_page(request):
    context = {}

    categories = Category.objects.select_related('product_set').all()
    popular_models = Product.objects.order_by('-views').all()[:5]

    context['categories'] = categories
    context['popular_models'] = popular_models

    return render(request, 'mainpage/landing.html', context=context)
