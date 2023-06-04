from django.urls import path

from apps.telegram.views import *

urlpatterns = [
    path('webhook/', webhook),
    path('test_bot/', send_test_message),
    path('make_order/', order, name='make_order'),
    path('make_question/', question, name='make_question'),
]
