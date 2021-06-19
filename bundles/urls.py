from django.urls import path

from . import views
from .helpers import get_total_price

urlpatterns = [
    path('', views.bundles, name='bundles'),
    path('bundlecategories/', views.bundle_categories,
         name='bundle_categories'),
    path('withitems/<bundle_id>/', views.with_items, name='with_items'),
    path('gettotalprice/', get_total_price, name='get_total_price'),
]
