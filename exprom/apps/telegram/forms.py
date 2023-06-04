from django import forms

from apps.catalog.models import Product
from apps.telegram.models import OrderDB, QuestionDB


class OrderForm(forms.ModelForm):
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Почта', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(label='Телефон', widget=forms.TextInput(attrs={'class': 'form-control'}))
    model_number = forms.IntegerField(label='Номер модели', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    additional_info = forms.CharField(
        label='Дополнительная информация',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        required=False,
    )

    class Meta:
        model = OrderDB
        fields = (
            'first_name',
            'email',
            'phone',
            'model_number',
            'additional_info'
        )

    def clean_model_number(self):
        model_number = self.cleaned_data.get('model_number')
        if not Product.objects.filter(number=model_number).exists():
            self.add_error('model_number', 'Данной модели не существует')

        return model_number


class QuestionForm(forms.ModelForm):
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Почта', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(label='Телефон', widget=forms.TextInput(attrs={'class': 'form-control'}))
    text = forms.CharField(
        label='Текст вопроса',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        required=True,
    )

    class Meta:
        model = QuestionDB
        fields = (
            'first_name',
            'email',
            'phone',
            'text',
        )
