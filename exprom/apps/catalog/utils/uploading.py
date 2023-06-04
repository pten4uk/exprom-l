import os

from config.settings import MEDIA_ROOT


def upload_product_photo(instance, filename):
    if hasattr(instance, 'content_object'):
        instance = instance.content_object

    path = f'products/{instance.slug}/{filename}'
    full_path = os.path.join(MEDIA_ROOT, path)

    if not os.path.exists(full_path):
        return path
    else:
        os.remove(full_path)
        return path


def upload_material(instance, filename):
    path = f'materials/{filename}'
    full_path = os.path.join(MEDIA_ROOT, path)

    if not os.path.exists(full_path):
        return path
    else:
        os.remove(full_path)
        return path
