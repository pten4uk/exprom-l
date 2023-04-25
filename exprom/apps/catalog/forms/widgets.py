from django.forms import ClearableFileInput


class ProductPhotoInput(ClearableFileInput):
    template_name = "catalog/forms/widgets/product_photo_input.html"
