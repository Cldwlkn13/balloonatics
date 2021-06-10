from django.urls import path

from . import views

urlpatterns = [
    path('', views.bundles, name='bundles'),
    path('bundlecategories/', views.bundle_categories,
         name='bundle_categories'),
    path('withitems/<int:bundle_id>/', views.with_items, name='with_items'),
    path('serveimage/<int:product_id>/', views.serve_image,
         name='serve_image'),
]
