from apps.telegram.deps import Bot
from apps.telegram.models import BotAdminDB, OrderDB, QuestionDB


def send_bot_admin_message(message: str):
    """ Отправляет сообщение администраторам в телеграм от лица бота """

    recipients_chats = BotAdminDB.objects.get_messages_recipients().values_list('chat_id', flat=True)

    for chat_id in recipients_chats:
        Bot.send_message(chat_id, message, parse_mode='HTML')


def send_new_order_to_admins(order: OrderDB):
    """ Отправляет заявку в телеграм ко всем администраторам бота """

    text = '<b>Новая заявка!</b>'
    text += '\n'

    text += f'\nИмя: {order.first_name}'
    text += f'\nПочта: {order.email}'
    text += f'\nТелефон: {order.phone}'
    text += f'\nВыбранная модель: {order.model_number}'
    text += f'\nДополнительная информация: {order.additional_info}'

    send_bot_admin_message(text)


def send_new_question_to_admins(question: QuestionDB):
    """ Отправляет вопрос в телеграм ко всем администраторам бота """

    text = '<b>Новый вопрос!</b>'
    text += '\n'

    text += f'\nИмя: {question.first_name}'
    text += f'\nПочта: {question.email}'
    text += f'\nТелефон: {question.phone}'
    text += f'\nТекст вопроса: {question.text}'

    send_bot_admin_message(text)
