from django.urls import path

from . import views

urlpatterns = [
    path('', views.printing, name='printing'),
    path('load/', views.load_print_selector, name='load_print_selector'),
    path('order/', views.order, name='order'),
]