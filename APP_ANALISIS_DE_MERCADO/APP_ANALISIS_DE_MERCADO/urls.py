from django.contrib import admin
from django.urls import path, include
from .views import dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard, name='dashboard'),  # Ruta raíz
    path('accounts/', include('django.contrib.auth.urls')),  # URLs de autenticación de Django
    path('projects/', include('project_tasks.urls')),
]