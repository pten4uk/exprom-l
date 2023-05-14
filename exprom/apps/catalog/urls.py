from django.urls import path
from .views import *


urlpatterns = [
    # API
    path('api/search/', product_search),
    path('api/search_tags/', tag_search),

    path('<slug:category_slug>/', ProductList.as_view(), name='catalog_category'),
    path('<slug:category_slug>/<slug:product_slug>/', ProductDetail.as_view(), name='catalog_category_product'),
]
