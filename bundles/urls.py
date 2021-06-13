from django.urls import path

from . import views

urlpatterns = [
    path('', views.bundles, name='bundles'),
    path('bundlecategories/', views.bundle_categories,
         name='bundle_categories'),
    path('withitems/<bundle_id>/', views.with_items, name='with_items'),
    path('gettotalprice/', views.get_total_price, name='get_total_price'),
    path('serveimage/<int:product_id>/', views.serve_image,
         name='serve_image'),
]
