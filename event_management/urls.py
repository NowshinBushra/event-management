from django.contrib import admin
from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls
from core.views import home, no_permission
from events.views import dashboard
from django.conf import settings
from django.conf.urls.static import static

from events.views import test_media
from django.views.static import serve
from django.urls import re_path
urlpatterns = [
    
    re_path(
        r'^media/(?P<path>.*)$',
        serve,
        {'document_root': settings.MEDIA_ROOT},
    ),
    
    path('admin/', admin.site.urls),
    path('', include('events.urls')),
    path('', home, name='home'),
    path('events/', include('events.urls')),
    path('users/', include('users.urls')),
    path('dashboard/', dashboard, name='dashboard'),
    path('no-permission/', no_permission, name='no-permission'),
    path('test-media/', test_media)
] 
# + debug_toolbar_urls()
if settings.DEBUG:
    urlpatterns += debug_toolbar_urls()

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)