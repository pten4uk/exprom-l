from django import forms

from apps.catalog.forms.widgets import ProductPhotoInput
from apps.catalog.models import Product, Category, Photo


class ProductAdminForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        label='Категория',
        empty_label='Без категории',
        queryset=Category.objects.all(),
        required=False,
    )
    photo = forms.ImageField(label='Главное фото', widget=ProductPhotoInput())

    class Meta:
        model = Product
        fields = ('photo', 'category',)


class PhotoInlineAdminForm(forms.ModelForm):
    photo = forms.ImageField(label='Дополнительное фото', widget=ProductPhotoInput())

    class Meta:
        model = Photo
        fields = ('photo',)


class MaterialAdminForm(forms.ModelForm):
    photo = forms.ImageField(label='Фотография', widget=ProductPhotoInput())

