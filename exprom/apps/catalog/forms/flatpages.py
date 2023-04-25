from django import forms
from ckeditor.widgets import CKEditorWidget
from django.contrib.flatpages.models import FlatPage


class FlatpagesAdminForm(forms.ModelForm):
    content = forms.CharField(label='Описание', widget=CKEditorWidget())

    class Meta:
        model = FlatPage
        fields = ('content',)


