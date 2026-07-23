from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from tours_app import admin_views

urlpatterns = [
    path('admin/reports/', admin_views.reports, name='admin_reports'),
    path('admin/activity-logs/', admin_views.activity_logs, name='admin_activity_logs'),
    path('admin/help/', admin_views.help_support, name='admin_help_support'),
    path('admin/', admin.site.urls),
    path('', include('tours_app.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
