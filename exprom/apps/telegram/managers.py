from django.db import models
from django.db.models import QuerySet

from apps.telegram.exceptions import OnlyOneObjectError


class BotDBManager(models.Manager):
    def create(self, **kwargs):
        """
        Создает объект бота, если он не существует.
        Иначе выбрасывает исключение OnlyOneObjectError
        """

        if self.exists():
            raise OnlyOneObjectError()
        return super().create(**kwargs)

    def update_bot(self, **kwargs):
        """
        Обновляет информацию, если объект уже существует,
        или создает объект, если его нет
        """

        obj = self.first()

        if obj is None:
            obj = self.model(**kwargs)
            obj.save()
        else:
            self.update(**kwargs)


class BotAdminDBManager(models.Manager):
    def get_messages_recipients(self) -> QuerySet:
        """ Возвращает QuerySet из тех пользователей, кому можно отправлять уведомления в чат """

        return self.filter(is_verified=True)
