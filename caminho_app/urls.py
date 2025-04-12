from django.urls import path
from .views import processar_algoritmo

urlpatterns = [
    path('', processar_algoritmo, name='processar_algoritmo'),
]
