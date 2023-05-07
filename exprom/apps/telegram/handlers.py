from telebot import types

from apps.telegram.deps import Bot
from apps.telegram.models import BotDB, BotAdminDB


def _start(message: types.Message):
    """
    Регистрирует нового администратора.
    После отправки заявки, необходимо подтвердить ее через админ панель.
    """

    chat_id = message.chat.id
    user = message.from_user

    bot_admin = BotAdminDB.objects.filter(chat_id=chat_id).first()

    if bot_admin is not None:
        text = 'Вы уже отправили заявку на регистрацию. Необходимо подтвердить заявку через админпанель'
        Bot.send_message(chat_id, text)
    else:
        BotAdminDB.objects.create(
            chat_id=chat_id,
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
            bot=BotDB.objects.first()
        )
        text = 'Заявка на регистрацию отправлена. Необходимо подтвердить заявку через админпанель'
        Bot.send_message(chat_id, text)


def _new_message(message: types.Message):
    Bot.delete_message(message.chat.id, message_id=message.message_id)


def register_handlers():
    Bot.register_message_handler(_start, commands=['start'])
    Bot.register_message_handler(_new_message)
