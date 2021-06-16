from django.urls import path

from . import views

urlpatterns = [
    path('', views.printing, name='printing'),
    path('load/', views.load_print_selector, name='load_print_selector'),
    path('newprintorder/', views.new_order_handler, name='new_order_handler'),
    path('updateprintorder/<custom_print_id>/', views.update_order_handler, name='update_order_handler'),
]