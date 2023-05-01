import debug_toolbar
from django.conf.urls.static import static

from config import settings
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('', include('apps.mainpage.urls')),
    path('exprom_admin/', admin.site.urls),
    path('catalog/', include('apps.catalog.urls')),
    path('pages/', include('django.contrib.flatpages.urls')),
]


if settings.DEBUG:
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
    urlpatterns.extend(static(settings.STATIC_URL, document_root=settings.STATIC_ROOT))
    urlpatterns.extend(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
