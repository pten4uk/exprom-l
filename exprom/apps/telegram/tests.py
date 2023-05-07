from django.test import TestCase

from apps.telegram.exceptions import OnlyOneObjectError
from apps.telegram.models import BotDB


class TelegramTestCase(TestCase):
    def test_only_one_bot_created(self):
        """ Проверяет возможность создания только одного объекта класса BotDB """

        with self.assertRaises(OnlyOneObjectError):
            BotDB.objects.create(id=1)
            BotDB.objects.create(id=2)

    def test_dont_save_second_bot_instance(self):
        """ Проверяет невозможность сохранения второго объекта через метод save() """

        with self.assertRaises(OnlyOneObjectError):
            BotDB.objects.create(id=1)

            bot = BotDB(id=2)
            bot.save()

    def test_update_bot(self):
        pk = 1

        BotDB.objects.create(id=pk)
        BotDB.objects.update_bot(id=pk)

        bot = BotDB.objects.first()
        self.assertTrue(bot.pk, pk)


