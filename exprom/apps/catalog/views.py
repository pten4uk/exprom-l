from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView

from .models import Product, Category


class ProductList(ListView):
    model = Product
    template_name = 'catalog/catalog.html'
    context_object_name = 'models'

    @staticmethod
    def _get_category_by_slug(slug: str):
        return Category.objects.filter(slug=slug).first()

    @staticmethod
    def _get_first_category() -> Category:
        return Category.objects.first()

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug', None)
        category = self._get_category_by_slug(category_slug)

        if category is None:
            return redirect(reverse("catalog_category", args=(self._get_first_category().slug, )))

        return super().get_queryset().filter(category=category)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['chosen_category_slug'] = self.kwargs.get('category_slug', None)
        return context


class ProductDetail(DetailView):
    model = Product
    slug_url_kwarg = 'product_slug'
    template_name = 'catalog/model_detail/model.html'
    context_object_name = 'model'
