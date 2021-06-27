from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home'), 
    path('terms', views.terms_and_conditions, name='terms_and_conditions')
]
