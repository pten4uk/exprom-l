import os

from django.conf import settings
from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib.sites.models import Site
from django.utils.safestring import mark_safe

from .forms.model_forms import ProductAdminForm, PhotoInlineAdminForm, MaterialAdminForm
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


class TagInline(admin.TabularInline):
    model = Tag
    fields = ('name', )
    extra = 1


class ProductPropertyValueInline(admin.TabularInline):
    model = ProductPropertyValue
    fields = ('value', 'product_property')
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    readonly_fields = ('slug',)
    fields = ('name', 'slug', 'description')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    inlines = [PhotoInline, TagInline, ProductPropertyValueInline]
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


@admin.register(MaterialCategory)
class MaterialCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(MaterialLayout)
class MaterialAdmin(admin.ModelAdmin):
    form = MaterialAdminForm
    list_display = ('name', 'category', 'get_photo')

    @admin.display(description='Фотография')
    def get_photo(self, obj: MaterialLayout):
        photo = obj.get_photo()
        url = None

        if photo:
            url = photo.url

        return mark_safe(f'<img src="{url}" width="100px">')


@admin.register(ProductProperty)
class ProductPropertyAdmin(admin.ModelAdmin):
    pass

# -------------------------------------------------Developer Mode-------------------------------------------------------


if settings.DEBUG:
    admin.site.register(Photo)

    admin.site.site_title = 'exprom-l (DEV)'
    admin.site.site_header = 'exprom-l (DEV)'
