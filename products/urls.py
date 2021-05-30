from django.urls import path

from . import views

urlpatterns = [
    path('', views.products, name='products'),
    path('categories/', views.categories, name='categories'),
    path('sub_categories/', views.sub_categories, name='sub_categories'),
    path('<int:product_id>/', views.product_detail, name='product_detail'),
]
