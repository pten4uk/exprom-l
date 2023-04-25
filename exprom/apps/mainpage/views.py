from django.shortcuts import render

from apps.catalog.models import Category


def main_page(request):
    context = {}
    categories = Category.objects.all()
    context['categories'] = categories
    return render(request, 'mainpage/landing.html', context=context)
