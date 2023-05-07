from django.contrib import admin

from apps.telegram.models import BotDB, BotAdminDB, OrderDB


@admin.register(BotAdminDB)
class BotAdminDBAdmin(admin.ModelAdmin):
    fields = ('chat_id', 'first_name', 'last_name', 'get_username', 'is_verified')
    list_display = ('get_username', 'first_name', 'last_name', 'is_verified')
    readonly_fields = ('chat_id', 'first_name', 'last_name', 'get_username')

    def save_model(self, request, obj, form, change):
        """
        Сохраняет модель только если ее изменяют.
        Через админку запрещено создавать объекты администраторов.
        Только через заявку телеграма.
        """

        if change:
            super().save_model(request, obj, form, change)

    @admin.display(description='Имя пользователя')
    def get_username(self, obj: BotDB):
        return f'@{obj.username}'


@admin.register(BotDB)
class BotDBAdmin(admin.ModelAdmin):
    change_form_template = 'telegram/admin/change_form.html'
    fields = ('id', 'first_name', 'last_name', 'get_username')
    list_display = ('first_name', 'get_username')
    readonly_fields = ('id', 'first_name', 'last_name', 'get_username')

    def save_model(self, request, obj, form, change):
        # убираем возможность создания новых моделей бота через админпанель
        pass

    @admin.display(description='Имя пользователя')
    def get_username(self, obj: BotDB):
        return f'@{obj.username}'


@admin.register(OrderDB)
class OrderDBAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone', 'model_number')
    fields = ('first_name', 'email', 'phone', 'model_number', 'additional_info', 'admin_notes',)
    readonly_fields = ('first_name', 'email', 'phone', 'model_number', 'additional_info',)

    def save_model(self, request, obj, form, change):
        # убираем возможность создания новых моделей заказа через админпанель

        if change:
            super().save_model(request, obj, form, change)

