from django.db import models

from apps.telegram.exceptions import OnlyOneObjectError
from apps.telegram.managers import BotDBManager, BotAdminDBManager


class BotDB(models.Model):
    """ Отображение информации Телеграм Бота в БД """

    id = models.BigIntegerField('Идентификатор', primary_key=True)
    first_name = models.CharField('Имя', max_length=60, blank=True, null=True)
    last_name = models.CharField('Фамилия', max_length=60, blank=True, null=True)
    username = models.CharField('Имя пользователя', max_length=60, blank=True, null=True)

    objects = BotDBManager()

    class Meta:
        verbose_name = 'Телеграм бот'
        verbose_name_plural = 'Телеграм боты'

    def __str__(self):
        return f'{self.username}'

    def save(self, **kwargs):
        obj: BotDB = self.__class__.objects.first()

        # если уже существует в базе
        if obj is not None:
            # если текущий объект уже создан
            if obj.pk != self.pk:
                raise OnlyOneObjectError()

        return super().save(**kwargs)


class BotAdminDB(models.Model):
    """ Администратор бота, которому приходят все уведомления от него """

    bot = models.ForeignKey(BotDB, related_name='bot_admins', on_delete=models.CASCADE)
    chat_id = models.BigIntegerField('Идентификатор чата с ботом', unique=True)
    first_name = models.CharField('Имя', max_length=60, blank=True, null=True)
    last_name = models.CharField('Фамилия', max_length=60, blank=True, null=True)
    username = models.CharField('Имя пользователя', max_length=60, blank=True, null=True)

    is_verified = models.BooleanField('Подтвержден', default=False)

    objects = BotAdminDBManager()

    class Meta:
        verbose_name = 'Администратор бота'
        verbose_name_plural = 'Администраторы бота'

    def __str__(self):
        return f'{self.chat_id}'

    def get_chat_id(self):
        return self.chat_id

    def verify(self):
        self.is_verified = True
        self.save()


class OrderDB(models.Model):
    """ Заказ через онлайн заявку """

    first_name = models.CharField('Имя', max_length=60)
    email = models.EmailField('Почта')
    phone = models.CharField('Телефон', max_length=20)
    model_number = models.IntegerField('Номер модели')
    additional_info = models.TextField('Дополнительная информация', blank=True, null=True)
    admin_notes = models.TextField('Пометки администратора', blank=True, null=True)

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'

    def __str__(self):
        return f'Заказ от: {self.email}'


class QuestionDB(models.Model):
    """ Вопрос через онлайн заявку """

    first_name = models.CharField('Имя', max_length=60)
    email = models.EmailField('Почта')
    phone = models.CharField('Телефон', max_length=20)
    text = models.TextField('Текст', max_length=2000)

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self):
        return f'Вопрос от: {self.email}'
