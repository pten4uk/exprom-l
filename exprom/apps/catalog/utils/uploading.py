import os

from config.settings import MEDIA_ROOT


def upload_function(instance, filename):
    if hasattr(instance, 'content_object'):
        instance = instance.content_object

    path = f'products/{instance.slug}/{filename}'
    full_path = os.path.join(MEDIA_ROOT, path)

    if not os.path.exists(full_path):
        return path
    else:
        os.remove(full_path)
        return path
