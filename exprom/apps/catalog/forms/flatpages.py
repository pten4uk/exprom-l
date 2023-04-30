from django import forms
from ckeditor.widgets import CKEditorWidget
from django.contrib.flatpages.models import FlatPage


class FlatpagesAdminForm(forms.ModelForm):
    url = forms.CharField(help_text='У ссылки нужно с двух сторон указать слеши. Например: "/about/"')
    content = forms.CharField(label='Описание', widget=CKEditorWidget())

    class Meta:
        model = FlatPage
        fields = ('content',)
