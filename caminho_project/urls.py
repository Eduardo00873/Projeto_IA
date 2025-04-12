from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('caminho_app.urls')),  # Substitui "tua_app" pelo nome real
]
