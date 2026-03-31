from django.contrib import admin
from django.urls import path, include
<<<<<<< HEAD
from django.conf import settings
from django.conf.urls.static import static
=======
>>>>>>> 3c621a99564f3dba48ef5ff875bc43d157a8466d

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('planner.urls')),
]
<<<<<<< HEAD

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
=======
>>>>>>> 3c621a99564f3dba48ef5ff875bc43d157a8466d
