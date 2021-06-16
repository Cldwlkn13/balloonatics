from django.urls import path
from . import views


urlpatterns = [
    path('', views.view_cart, name='view_cart'),
    path('addproduct/<item_id>/', views.add_product_to_cart, name='add_product_to_cart'),
    path('updateproduct/<item_id>/', views.update_product_cart, name='update_product_cart'),
    path('removeproduct/<item_id>/', views.remove_product_from_cart, name='remove_product_from_cart'),
    path('addbundle/', views.add_bundle_to_cart, name='add_bundle_to_cart'),
    path('updatebundle/<bundle_id>/', views.update_bundle_in_cart, name='update_bundle_in_cart'),
    path('removebundle/<bundle_id>/', views.remove_bundle_from_cart, name='remove_bundle_from_cart'),
    path('removecustomprintorder/<custom_print_id>/', views.remove_custom_print_order_from_cart,
            name='remove_custom_print_order_from_cart'),
]
