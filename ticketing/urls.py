from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API routes
    path('api/events/', include('events.urls')),
    path('api/users/', include('users.urls')),
    path('api/tickets/', include('tickets.urls')),
]

# Only serve media files locally when DEBUG=True
# (In production on Render, Cloudinary handles all images)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)