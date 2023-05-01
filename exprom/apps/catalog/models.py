import os.path

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import QuerySet

from .utils import upload_function
from .utils.process_photo import PhotoFormatter
from .utils.slug import slugify
from .utils.uploading import upload_material


class Category(models.Model):
    name = models.CharField('Название', max_length=100, unique=True)
    slug = models.SlugField('Название ссылки', max_length=100, blank=True, unique=True)
    description = models.TextField('Описание', max_length=600, default='')

    objects = models.Manager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def save(self, *args, **kwargs):
        self.name: str
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    number = models.PositiveSmallIntegerField('Номер', primary_key=True)
    name = models.CharField(
        'Короткое название',
        help_text='Короткое название, которое будет отображаться перед номером модели',
        max_length=30,  # одинаково со slug
        unique=True,
    )
    slug = models.SlugField('Имя ссылки', max_length=30, unique=True)
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        null=True,
        blank=True,
        default=None,
        on_delete=models.SET_DEFAULT,
    )
    photo = models.ImageField('Главное фото', upload_to=upload_function, null=True, blank=True)  # добавить валидатор для соотношения сторон фотографии
    shirt_description = models.CharField('Краткое описание', max_length=50, blank=True, default='')
    description = models.TextField('Описание', blank=True)
    width = models.PositiveSmallIntegerField('Ширина')
    height = models.PositiveSmallIntegerField('Высота')
    depth = models.PositiveSmallIntegerField('Глубина')
    price = models.PositiveSmallIntegerField('Цена')

    # количество просмотров продукта (заходы на детальную страницу)
    views = models.PositiveBigIntegerField(default=0)

    objects = models.Manager()

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['number']

    def __str__(self):
        return f'{self.category} {self.number}'

    def save(self, *args, **kwargs):
        # добавляем слаг
        self.name: str
        self.slug = slugify(self.name)

        super().save(*args, **kwargs)

        if self.photo:
            PhotoFormatter(self.photo.path).save()

    def get_name(self):
        """ Возвращает имя для репрезентации модели """

        return f'{self.name} {self.number}'

    def get_photo(self):
        if self.photo:
            if not os.path.exists(self.photo.path):
                self.photo = None
                self.save()
            return self.photo

    def add_view(self):
        """ Добавляет один просмотр к данному объекту """

        self.views += 1
        self.save()

    def get_additional_photos(self):
        """
        Получает полный список объектов дополнительных фотографий,
        и проверяет существуют ли сами фотографии
        """

        photos: QuerySet[Photo] = Photo.objects.filter(object_id=self.pk)

        for photo in photos:
            photo.check_photo_exists()

        return photos


class Photo(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    photo = models.ImageField('Изображение', upload_to=upload_function)

    objects = models.Manager()

    def __str__(self):
        return f'Изображение {self.pk} для {self.content_object}'

    class Meta:
        verbose_name = 'Фото'
        verbose_name_plural = 'Фото'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.photo:
            PhotoFormatter(self.photo.path).save()

    def check_photo_exists(self):
        """ Проверяет, существует ли фотография и удаляет объект, если не существует """

        if self.photo and not os.path.exists(self.photo.path):
            self.delete()


class MaterialCategory(models.Model):
    name = models.CharField('Имя', max_length=60)
    description = models.CharField('Описание', max_length=500, default='', blank=True)

    objects = models.Manager()

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Категория материала'
        verbose_name_plural = 'Категории материала'


class Material(models.Model):
    """ Материал обивки модели """

    name = models.CharField('Имя', max_length=30)
    photo = models.ImageField('Фотография', upload_to=upload_material)
    category = models.ForeignKey('MaterialCategory', verbose_name='Категория', on_delete=models.CASCADE)

    objects = models.Manager()

    class Meta:
        verbose_name = 'Материал'
        verbose_name_plural = 'Материалы'

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.photo:
            PhotoFormatter(self.photo.path).save()

    def get_photo(self):
        if self.photo:
            if not os.path.exists(self.photo.path):
                self.photo = None
                self.save()
            return self.photo


