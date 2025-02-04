
from django.contrib import admin
from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls
# from events.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('events.urls')),
    path('events/', include('events.urls')),
    # path('participants', include('participants.urls')),
] + debug_toolbar_urls()
