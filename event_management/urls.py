from django.contrib import admin
from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls
from core.views import home, no_permission
from events.views import dashboard
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('events.urls')),
    path('', home, name='home'),
    path('events/', include('events.urls')),
    path('users/', include('users.urls')),
    path('dashboard/', dashboard, name='dashboard'),
    path('no-permission/', no_permission, name='no-permission')
] + debug_toolbar_urls()

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)