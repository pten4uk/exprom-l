from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage

from apps.catalog.forms.flatpages import FlatpagesAdminForm


class CustomFlatPageAdmin(FlatPageAdmin):
    form = FlatpagesAdminForm
    list_display = ('title', 'url')
    fieldsets = (
        (None, {'fields': ('url', 'title', 'content', 'sites')}),

        # раскомментировать, если нужно будет дать возможность указать расширенные настройки
        # (_('Advanced options'), {
        #     'classes': ('collapse',),
        #     'fields': (
        #         'registration_required',
        #         'template_name',
        #     ),
        # }),

    )


admin.site.unregister(FlatPage)
admin.site.register(FlatPage, CustomFlatPageAdmin)
