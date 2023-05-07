from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from telebot.types import Update

from apps.telegram.admin import BotDBAdmin
from apps.telegram.deps import Bot
from apps.telegram.forms import OrderForm
from apps.telegram.models import BotAdminDB, OrderDB
from apps.telegram.utils import send_bot_admin_message, send_new_order_to_admins


@csrf_exempt
def webhook(request: HttpRequest):
    body = request.body.decode('utf8')
    Bot.process_new_updates(updates=[Update.de_json(body)])
    return HttpResponse()


def send_test_message(request: HttpRequest):
    """ Отправляет тестовое сообщение от лица бота в чаты, для проверки его работоспособности """

    message = 'Тестовое сообщение, говорящее о работоспособности бота. '\
              'И то, что вы добавлены в список получателей сообщений.'
    send_bot_admin_message(message)

    return HttpResponse()


def order(request: HttpRequest):
    if request.method == 'POST':
        form = OrderForm(request.POST)

        if form.is_valid():
            obj: OrderDB = form.save()
            message = 'Заявка успешно отправлена! В ближайшее время с Вами свяжется наш менеджер.'
            send_new_order_to_admins(obj)
            messages.success(request, message)
        else:
            for field in form:
                for error in field.errors:
                    messages.error(request, f'Ошибка валидации поля "{field.label}": {error}')

        return redirect('mainpage')
