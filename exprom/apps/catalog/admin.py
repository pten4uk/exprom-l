import os

from django.conf import settings
from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib.sites.models import Site
from django.utils.safestring import mark_safe

from .forms.model_forms import ProductAdminForm, PhotoInlineAdminForm
from .models import *

admin.site.unregister(Group)
admin.site.unregister(User)
admin.site.unregister(Site)

admin.site.site_title = 'Администрирование Экспром-Л'
admin.site.site_header = 'Администрирование Экспром-Л'


class PhotoInline(GenericTabularInline):
    model = Photo
    form = PhotoInlineAdminForm
    verbose_name = 'Дополнительное фото'
    verbose_name_plural = 'Дополнительные фото'
    extra = 0

    def get_queryset(self, request):
        qs = super().get_queryset(request).prefetch_related('content_object', 'content_type')
        pks = []
        for image in qs:
            if image.photo and not os.path.exists(image.photo.path):
                pks.append(image.pk)
        Photo.objects.filter(pk__in=pks).delete()
        qs = qs.exclude(pk__in=pks)
        return qs


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    readonly_fields = ('slug',)
    fields = ('name', 'slug', 'description')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    inlines = [PhotoInline]
    list_select_related = True
    list_display = ('get_str_title', 'category', 'shirt_description', 'price', 'get_photo')
    fields = (
        'number',
        'name',
        'category',
        'photo',
        'shirt_description',
        'description',
        ('width', 'height'),
        'depth',
        'price',
    )
    list_filter = ('category',)
    ordering = ('number',)

    def get_object(self, request, object_id, from_field=None):
        obj = Product.objects.select_related('category').get(pk=object_id)
        if obj.photo and not os.path.exists(obj.photo.path):
            obj.photo = None
        return obj

    @admin.display(description='Название')
    def get_str_title(self, obj):
        return f'{obj.name} {obj.number}'

    @admin.display(description='Главная фотография')
    def get_photo(self, obj: Product):
        photo = obj.get_photo()
        url = None

        if photo:
            url = photo.url

        return mark_safe(f'<img src="{url}" width="100px">')


# -------------------------------------------------Developer Mode-------------------------------------------------------


if settings.DEBUG:
    admin.site.register(Photo)

    admin.site.site_title = 'exprom-l (DEV)'
    admin.site.site_header = 'exprom-l (DEV)'
