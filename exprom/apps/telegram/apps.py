import logging

from django.apps import AppConfig
from django.db import ProgrammingError

from config.settings import TELEGRAM_WEBHOOK_URL

logger = logging.getLogger(__name__)


class TelegramConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.telegram'
    verbose_name = 'Телеграм'

    def ready(self):
        from apps.telegram.deps import Bot
        from apps.telegram.handlers import register_handlers
        from apps.telegram.models import BotDB

        logger.info('Запускаем телеграм бота...')
        webhook_url = Bot.get_webhook_info().url

        if webhook_url != TELEGRAM_WEBHOOK_URL:
            Bot.remove_webhook()
            Bot.set_webhook(url=TELEGRAM_WEBHOOK_URL)

        register_handlers()
        logger.info('Бот успешно запущен!')

        bot_info = Bot.get_me()

        try:
            BotDB.objects.update_bot(
                id=bot_info.id,
                first_name=bot_info.first_name,
                last_name=bot_info.last_name,
                username=bot_info.username
            )
        except ProgrammingError:
            # отслеживаем исключение на случай, если таблица бота в базе еще не создана
            pass

