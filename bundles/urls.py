from django.urls import path

from . import views

urlpatterns = [
    path('', views.bundles, name='bundles'),
    path('serveimage/<int:product_id>/', views.serve_image,
         name='serve_image'),
]
