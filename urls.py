from django.contrib import admin
from django.urls import path, include
from user_management import views as user_views
from external_integration import views as ext_views
from job_market import views as job_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', user_views.home, name='home'),
    path('import-jobs/', ext_views.import_jobs, name='import_jobs'),
    path('dashboard/', job_views.dashboard, name='dashboard'),
]