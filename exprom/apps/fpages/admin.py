from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.utils.translation import gettext_lazy as _

from apps.catalog.forms.flatpages import FlatpagesAdminForm


class CustomFlatPageAdmin(FlatPageAdmin):
    form = FlatpagesAdminForm
    list_display = ('title', 'url')
    fieldsets = (
        (None, {'fields': ('url', 'title', 'content', 'sites')}),
        (_('Advanced options'), {
            'classes': ('collapse',),
            'fields': (
                'registration_required',
                'template_name',
            ),
        }),
    )


admin.site.unregister(FlatPage)
admin.site.register(FlatPage, CustomFlatPageAdmin)
