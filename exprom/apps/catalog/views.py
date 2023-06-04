from django.http import JsonResponse, HttpRequest
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView

from .models import Product, Category, MaterialCategory, Tag


class AllProducts(ListView):
    """ Полный список товаров отсортированный по номеру модели """

    model = Product
    context_object_name = 'models'
    queryset = Product.objects.all()
    ordering = ('number',)
    template_name = 'catalog/all_models.html'


class ProductList(ListView):
    """ Список товаров отфильтрованный по категории """

    model = Product
    queryset = Product.objects.select_related('category', 'properties').all()
    paginate_by = 15
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
            return redirect(reverse("catalog_category", args=(self._get_first_category().slug,)))

        return super().get_queryset().filter(category=category)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['chosen_category_slug'] = self.kwargs.get('category_slug', None)
        return context


class ProductDetail(DetailView):
    model = Product
    slug_url_kwarg = 'product_slug'
    template_name = 'catalog/model_detail/model_detail.html'
    context_object_name = 'model'

    def get(self, request, *args, **kwargs):
        obj: Product = self.get_object()
        obj.add_view()
        return super(ProductDetail, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['material_categories'] = MaterialCategory.objects.all()
        return context


# API
def product_search(request: HttpRequest):
    search = request.GET.get('search', '')
    qs = Product.objects.filter(tags__name__icontains=search).distinct()
    data = []

    for product in qs:
        serialized_product = {
            'pk': product.pk,
            'slug': product.slug,
            'category_slug': product.category.slug,
            'get_name': product.get_name(),
            'name': product.name,
            'number': product.number,
            'price': product.price,
            'photo': product.photo.url,
            'shirt_description': product.shirt_description,
            'description': product.description,
            'width': product.width,
            'height': product.height,
            'depth': product.depth,
        }
        data.append(serialized_product)

    return JsonResponse(data=data, safe=False)


def tag_search(request: HttpRequest):
    search = request.GET.get('search', '')
    qs = Tag.objects.filter(name__icontains=search)
    data = []

    for tag in qs:
        tag: Tag

        serialized_tag = {
            'id': tag.pk,
            'name': tag.name
        }
        data.append(serialized_tag)

    return JsonResponse(data=data, safe=False)
