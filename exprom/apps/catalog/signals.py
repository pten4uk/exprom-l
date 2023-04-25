import os

from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver

from .models import *


@receiver(pre_delete, sender=Product)
def delete_related_photos_on_delete(sender, instance, created=None, **kwargs):
    photo = instance.photo or None
    related_photos = Photo.objects.filter(object_id=instance.pk)

    if photo:
        os.remove(photo.path)

    if related_photos:
        for image in related_photos:
            os.remove(image.photo.path)


@receiver(post_save, sender=Product)
def delete_related_photos_on_save(sender, instance, created=None, **kwargs):
    if created is not None and created:
        photo = instance.photo or None
        related_photos = Photo.objects.filter(object_id=instance.pk)

        if not photo:
            os.remove(photo.path)

        for image in related_photos:
            if not image.photo:
                os.remove(image.photo.path)
