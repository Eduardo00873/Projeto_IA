from django.contrib import admin
from django.urls import path, include
from caminho_app.views import detectar_matricula_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('caminho_app.urls')),  # Substitui "tua_app" pelo nome real
    path('detetar-matricula/', detectar_matricula_view, name='detectar_matricula'),
]
