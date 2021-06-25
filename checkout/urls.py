from django.urls import path
from .webhooks import webhook

from . import views

urlpatterns = [
     path('', views.checkout, name='checkout'),
     path('checkout_success/<order_id>/',
         views.checkout_success,
         name='checkout_success'),
     path('validateorder/', views.validate_order, 
          name='validate_order'),
     path('cache_checkout_data/',
         views.cache_checkout_data,
         name='cache_checkout_data'),
     path('wh/', webhook, name='webhook'),
]