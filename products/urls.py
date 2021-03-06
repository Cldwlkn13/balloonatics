from django.urls import path

from . import views
from .helpers import serve_image

urlpatterns = [
    path('', views.products, name='products'),
    path('categories/', views.categories, name='categories'),
    path('sub_categories/', views.sub_categories, name='sub_categories'),
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    path('load_products/', views.load_products, name='load_products'),
    path('add/', views.add_product, name='add_product'),
    path('edit/', views.edit_product, name='edit_product'),
    path('delete/<int:product_id>/', views.delete_product,
         name='delete_product'),
    path('serveimage/<int:product_id>/', serve_image,
         name='serve_image'),
]
